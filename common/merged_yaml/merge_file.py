import os
import subprocess
import time
import urllib.parse
from curl_cffi import requests
from loguru import logger


def merge_yaml():
    process = subprocess.Popen(['common/merged_yaml/subconverter_win64/subconverter/subconverter.exe'])
    time.sleep(1)
    folder_path = 'common/merged_yaml/yaml_list'
    path_list = []
    for item in os.listdir(folder_path):
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
    result = subprocess.run(['node', 'common/merged_yaml/clash_proxy/format_conversion.js'], capture_output=True, text=True,
                            encoding='utf-8')
    # logger.info(result.stdout)
    logger.success('订阅文件转换成功')
    process.terminate()
    process.wait()
