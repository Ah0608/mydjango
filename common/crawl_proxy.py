from time import sleep

from curl_cffi import requests

from common.merged_yaml.auto_import_proxy import merge_and_import_proxy
from common.merged_yaml.check_proxy import check_socks_proxy
from common.merged_yaml.crawl_yaml_file import freeclashnode


def crawl():
    pass
    # sleep(10)
    # res = requests.get(url='http://127.0.0.1:8000/proxypool/allproxy/').json()
    # ips = res['data']
    # ip_num = len(ips)
    # print(f'代理池现有ip个数{ip_num}')
    # freeclashnode()
    # sleep(5)
    # times = 1
    # while times <= 3:
    #     try:
    #         merge_and_import_proxy()
    #         sleep(5)
    #         check_socks_proxy()
    #         break
    #     except FileNotFoundError as e:
    #         print(e)
    #         times += 1
