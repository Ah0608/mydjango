from pathlib import Path

import psutil
import signal
import os
import subprocess
import time
import urllib.parse
from curl_cffi import requests
from loguru import logger


def merge_yaml(all_files=[]):
    process = subprocess.Popen(['common/merged_yaml/subconverter_win64/subconverter/subconverter.exe'])
    time.sleep(1)
    folder_path = 'common/merged_yaml/yaml_list'
    path_list = []
    for item in all_files:
        item_path = os.path.join(folder_path, item)
        absolute_path = os.path.abspath(item_path)
        path_list.append('\"' + absolute_path + '\"')
        logger.info(absolute_path)
    path_list_str = '|'.join(path_list)
    encoded_filepath = urllib.parse.quote(path_list_str)
    url = f'http://127.0.0.1:25500/sub?target=clash&url={encoded_filepath}&insert=false'
    logger.info('请求url：{}'.format(url))
    res = requests.get(url)
    with open(r'common/merged_yaml/clash_proxy/before_conversion.txt', 'w', encoding='utf-8') as f:
        f.write(res.text)
    logger.success('合并文件已写入')
    logger.info('开始转换yaml文件')
    time.sleep(1)
    result = subprocess.run(['node', 'common/merged_yaml/clash_proxy/format_conversion.js'], capture_output=True, text=True,encoding='utf-8')
    if result.returncode == 0:
        logger.success('订阅文件转换成功')
    else:
        raise RuntimeError('订阅文件转换失败')
    process.terminate()
    process.wait()


def find_pid_by_name(process_name):
    """找到进程名称为 process_name 的进程的 PID"""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None


def kill_process_by_pid(pid):
    """杀死指定 PID 的进程"""
    try:
        os.kill(pid, signal.SIGTERM)  # 或者使用 signal.SIGKILL
        logger.info(f"进程 {pid} 已被杀死")
    except OSError as e:
        logger.info(f"杀死进程 {pid} 失败: {e}")


def auto_import_proxy():
    process_name = "socks_pool_start.exe"  # 将此处替换为目标进程名称
    pid = find_pid_by_name(process_name)
    if pid:
        logger.info(f"找到进程 {process_name} 的 PID: {pid}")
        kill_process_by_pid(pid)
    else:
        logger.info(f"未找到进程 {process_name}")
        command = [
            "common/merged_yaml/socks_pool_start.exe",
            "-f",
            "common/merged_yaml/config.yaml"
        ]
        try:
            logger.info('代理程序启动中...')
            subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            pid = find_pid_by_name(process_name)
            if pid:
                logger.info('代理程序启动成功')
            else:
                raise RuntimeError('启动失败')
        except:
            raise RuntimeError('节点导入失败')


def merge_and_import_proxy():
    relative_path = Path('common/merged_yaml/config.yaml')
    try:
        relative_path.unlink()
        print(f"{relative_path} 已删除")
    except FileNotFoundError:
        print("文件未找到")
    except PermissionError:
        print("没有权限删除文件")
    except Exception as e:
        print(f"发生错误: {e}")

    folder_path = 'common/merged_yaml/yaml_list'
    yaml_files = os.listdir(folder_path)

    yaml_lists = []
    for file in yaml_files:
        yaml_lists.append(file)
        logger.info(f'正在合并文件：{yaml_lists}')
        try:
            merge_yaml(yaml_lists)
        except Exception:
            logger.error(f"合并文件失败.已经排除文件{file}")
            yaml_lists.remove(file)
    logger.info(f'成功合并{yaml_lists}')
    auto_import_proxy()