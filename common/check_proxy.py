import time
from concurrent.futures import ThreadPoolExecutor

from curl_cffi import requests as req
from fake_useragent import UserAgent

from proxypool.models import ProxyPool

right_ips = []
check_url = ''


def RandomUserAgent():
    headers = {"User-Agent": UserAgent().chrome}
    return headers


def fetch_url(ip):
    global check_url
    print('{} --正在检测中请稍等...'.format(ip))
    proxy = {"http": ip, "https": ip}
    IP_RATING = 100
    retry_count = 0
    max_retries = 2
    speed_five = 0
    while retry_count < max_retries:
        try:
            start_time = time.time()
            response = req.get(url=check_url, proxies=proxy, headers=RandomUserAgent(), timeout=5,
                               impersonate='chrome110')
            response.raise_for_status()
            end_time = time.time()
            speed = end_time - start_time
            speed_five += speed
        except:
            IP_RATING = IP_RATING - 50
        retry_count = retry_count + 1
    if IP_RATING == 100:
        print(('{} --的评分是:{}').format(ip,IP_RATING))
        host = ip.split('://')[-1]
        type = ip.split('://')[0]
        avg_speed = round(speed_five / 5, 2)
        right_ips.append(ip)
        ProxyPool.objects.create(ip=host, type=type ,speed=avg_speed)


def multi_thread_check_proxy(url):
    global check_url
    check_url = url
    res = req.get('http://192.168.1.190:8000/sort').json()
    ips = [''.join(list(i.keys())) for i in res]
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(fetch_url, ips)
