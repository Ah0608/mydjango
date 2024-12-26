import os
import shutil
from datetime import datetime

from curl_cffi import requests
from parsel import Selector
from loguru import logger

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
proxies = {'http': 'socks5://192.168.1.171:1080', 'https': 'socks5://192.168.1.171:1080'}


def get_clash(url, proxies=None,headers=None):
    try:
        response = requests.get(url=url,proxies=proxies,headers=headers)
        if response.status_code == 200:
            return response
        else:
            raise RuntimeError(f"请求失败，状态码：{response.status_code}")
    except Exception:
        return False


def delete_all_files_in_directory(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        # 遍历目录中的所有文件和子目录
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                # 如果是文件则删除
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                # 如果是目录则删除目录及其内容
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.error(f"删除 {file_path} 时出错: {e}")
    else:
        logger.info(f"目录 {directory} 不存在或不是一个目录")
        exit()


def freeclashnode():
    date = datetime.now().strftime("%Y-%m-%d")
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    day = str(datetime.now().day)
    node_urls = [
        f'https://oneclash.githubrowcontent.com/{year}/{month.zfill(2)}/{year}{month.zfill(2)}{day.zfill(2)}.yaml',
        'https://proxy.v2gh.com/https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub',
        'https://raw.githubusercontent.com/ssrsub/ssr/master/ss-sub',
        'https://raw.githubusercontent.com/snakem982/proxypool/main/source/clash-meta.yaml',
        'https://raw.githubusercontent.com/snakem982/proxypool/main/source/clash-meta-2.yaml',
        'https://ghp.ci/https://raw.githubusercontent.com/free18/v2ray/refs/heads/main/c.yaml',
        'https://raw.githubusercontent.com/adiwzx/freenode/main/adispeed.yml',
    ]
    url = 'https://www.freeclashnode.com/free-node/'
    res = get_clash(url)
    sel = Selector(res.text)
    newday_url = 'https://www.freeclashnode.com' + sel.xpath(
        "//div[@class='panel-body']/div[1]//div[@class='item-heading pb-2']/a/@href").get(default='')
    res1 = get_clash(newday_url)
    sel1 = Selector(res1.text)
    yaml_url_list = sel1.xpath("//p[contains(text(),'ml')]/text()").getall()
    yaml_url_list.extend(node_urls)
    if yaml_url_list:
        delete_all_files_in_directory('common/merged_yaml/yaml_list')
        logger.success('文件清除成功')
        for index, yaml_url in enumerate(yaml_url_list):
            if index == 4 or index == 2:
                continue
            logger.info('正在请求：{}'.format(yaml_url))
            file_name = 'common/merged_yaml/yaml_list/{}_{}.yaml'.format(date, index)
            try:
                res = get_clash(yaml_url, proxies=proxies, headers=headers)
                yaml_content = res.text
            except Exception as e:
                logger.error('请求失败:{}'.format(e))
                continue
            with open(file_name, mode='w', encoding='utf-8', newline='') as file:
                file.write(yaml_content.strip())
                logger.success('{}下载成功'.format(file_name))
