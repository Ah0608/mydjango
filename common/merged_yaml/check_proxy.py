import socket
import time
from concurrent.futures import ThreadPoolExecutor

import psutil
from curl_cffi import requests
from loguru import logger
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydjango.settings')

import django

django.setup()

from proxypool.models import ProxyPool


def find_udp_ports_in_range(start: int = 42000, end: int = 45000) -> list:
    udp_ports = []
    for conn in psutil.net_connections(kind='udp'):
        if start <= conn.laddr.port <= end:
            udp_ports.append(conn.laddr.port)
    return list(set(udp_ports))


def get_local_ip():
    try:
        # 创建一个 UDP 套接字
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # 连接到一个公共的 IP 地址
        local_ip = s.getsockname()[0]  # 获取本地 IP 地址
        s.close()
        return local_ip
    except Exception as e:
        logger.info("获取本地 IP 地址失败:", e)
        return None


right_ips = []

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}


def fetch_url(ip):
    check_url = 'https://www.baidu.com/'
    logger.info('{} --正在检测中请稍等...'.format(ip))
    proxy = {"http": ip, "https": ip}
    IP_RATING = 100
    retry_count = 0
    max_retries = 2
    speed_five = 0
    while retry_count < max_retries:
        try:
            start_time = time.time()
            response = requests.get(url=check_url, proxies=proxy, headers=headers, timeout=10, impersonate='chrome110')
            response.raise_for_status()
            end_time = time.time()
            speed = end_time - start_time
            speed_five += speed
        except:
            IP_RATING = IP_RATING - 50
        retry_count = retry_count + 1
    logger.info(('{}--的评分是:{}').format(ip, IP_RATING))
    if IP_RATING == 100:
        host = ip.split('://')[-1]
        type = ip.split('://')[0]
        avg_speed = round(speed_five / 2, 2)
        try:
            right_ips.append(ip)
            ProxyPool.objects.create(ip=host, type=type, speed=avg_speed)
        except:
            logger.info('数据插入失败')
            pass


def check_socks_proxy():
    socks5_ports = find_udp_ports_in_range()
    local_ip = get_local_ip()
    socks_proxy = ['socks5://{}:{}'.format(local_ip, port) for port in socks5_ports]
    logger.info('共有{}个代理'.format(len(socks_proxy)))
    if len(socks_proxy) == 0:
        raise RuntimeError("没有找到可用的代理")
    logger.info(socks_proxy)
    ProxyPool.objects.all().delete()
    right_ips.clear()
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(fetch_url, socks_proxy)
    logger.info('可用的代理：\n{}\n共{}个'.format(right_ips,len(right_ips)))
    logger.info('代理检测结束!')