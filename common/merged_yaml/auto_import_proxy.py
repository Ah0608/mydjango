from pathlib import Path

import psutil
import signal
import os
import subprocess
import time
import urllib.parse
from curl_cffi import requests
from loguru import logger
from itertools import combinations


def merge_yaml(exclude_files=[]):
    process = subprocess.Popen(['common/merged_yaml/subconverter_win64/subconverter/subconverter.exe'])
    time.sleep(1)
    folder_path = 'common/merged_yaml/yaml_list'
    path_list = []
    for item in os.listdir(folder_path):
        if item not in exclude_files:
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
    subprocess.run(['node', 'common/merged_yaml/clash_proxy/format_conversion.js'], capture_output=True, text=True,
                            encoding='utf-8')
    logger.success('订阅文件转换成功')
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
    all_combinations = []

    for i in range(1, len(yaml_files) + 1):
        all_combinations.extend(combinations(yaml_files, i))
    for combo in all_combinations:
        try:
            logger.info(f"尝试排除文件组合: {combo}")
            merge_yaml(exclude_files=list(combo))
            auto_import_proxy()
            return
        except:
            logger.error(f"排除文件组合 {combo} 后仍然报错")
            logger.info(f"恢复文件组合 {combo} 的合并")