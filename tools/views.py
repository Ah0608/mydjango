import re
import subprocess

import pyfiglet
from django.http import JsonResponse
from django.shortcuts import render
from curl_cffi import requests

from django.views.decorators.csrf import csrf_exempt

ascii_art = pyfiglet.figlet_format("Awesome", font="slant")
print(ascii_art)


def get_external_ip():
    try:
        ip = requests.get('https://ident.me').text.strip()
        return ip
    except:
        return None


my_ip = get_external_ip()
print(my_ip)


def is_curl_command(command):
    curl_options = [
        r' -X ',  # 指定请求命令，如 -X POST
        r' -H ',  # 指定请求头，如 -H 'Content-Type: application/json'
        r' --data',  # 指定请求数据，如 --data '{"key":"value"}'
        r' --url',  # 指定请求 URL，如 --url 'http://example.com'
        r' --header',  # 指定请求头，如 --header 'Content-Type: application/json'
        r' --cookie',  # 指定请求 cookie，如 --cookie 'name=value'
        r' --compressed'  # 指定请求压缩，如 --compressed
    ]

    # 检查字符串是否以 curl 开头
    if not command.strip().startswith('curl'):
        return False

    # 检查字符串中是否包含任意一个典型的 curl 选项
    for option in curl_options:
        if re.search(option, command):
            return True

    return False


@csrf_exempt
def Curl(request):
    if request.method == 'POST':
        curl_command = request.POST.get('curl_command', '')
        if is_curl_command(curl_command):
            try:
                result = subprocess.run(
                    ['node', 'D:\workfile\PycharmProjects\mydjango\common\curl_converter\curl.js', curl_command],
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                if result.returncode == 0:
                    requests_code = result.stdout
                    return JsonResponse({'status': True, 'python_code': requests_code})
            except FileNotFoundError as e:
                return JsonResponse(
                    {'status': False, 'error_message': '文件名或扩展名太长。'})
        else:
            return JsonResponse(
                {'status': False, 'error_message': 'Invalid cURL command. Please enter a valid cURL command.'})
    else:
        return render(request, 'curl.html')


def List(request):
    online_tools = [
        {
            'url': 'https://www.spidertools.cn',
            'image': 'user/images/spidertools.png',
            'name': '爬虫工具库',
            'introduction': 'feapder 作者出品的爬虫工具库。'
        },
        {
            'url': 'https://spiderbox.cn/',
            'image': 'user/images/spiderbox.png',
            'name': 'SpiderBox',
            'introduction': '爬虫逆向资源导航站。'
        },
        {
            'url': 'https://www.kgtools.cn',
            'image': 'user/images/ktool.jpg',
            'name': 'K哥工具',
            'introduction': 'K哥爬虫出品,自研、收集各类爬虫实用工具。'
        },
        {
            'url': 'https://tool.chinaz.com',
            'image': 'user/images/zhanzhangtool.png',
            'name': '站长工具',
            'introduction': '功能齐全，SEO、各网站权重、友链、备案、IP 查询等等实用工具。'
        },
        {
            'url': 'https://spiderapi.cn',
            'image': 'user/images/spiderapi.png',
            'name': 'SpiderApi',
            'introduction': 'SpiderApi - 虫术 - 爬虫逆向常用 API。'
        },
        {
            'url': 'https://fontawesome.com',
            'image': 'user/images/fontawesome.svg',
            'name': 'Fontawesome图标',
            'introduction': '拥有30,000+ icon图标，可直接通过css引入。'
        },
        {
            'url': 'https://yesicon.app',
            'image': 'user/images/yesicon.svg',
            'name': 'yesIcon图标',
            'introduction': '200,000+ 枚高品质矢量图标 来自全球顶尖设计团队。'
        },
        {
            'url': 'https://chat18.aichatos.xyz',
            'image': 'user/images/aichatos.jpg',
            'name': 'AIchatOS',
            'introduction': '国内免费GPT3.5。'
        },
        {
            'url': 'https://greasyfork.org/zh-CN/scripts',
            'image': 'user/images/script.png',
            'name': 'Greasy Fork',
            'introduction': '各种全网视频去广告、百度云全网搜索等适用脚本。'
        },
        {
            'url': 'https://ipinfo.io/',
            'image': 'user/images/ipinfo.png',
            'name': 'IPinfo',
            'introduction': '根据ip查询国家地区信息。'
        },
        {
            'url': 'https://ai-bot.cn/best-free-ai-chatbots/',
            'image': 'user/images/ai-bot-square-logo.png',
            'name': 'AI工具集',
            'introduction': '各种ai工具的集合。'
        },
        {
            'url': 'https://jsoncrack.com/editor',
            'image': 'user/images/jsoncrack.ico',
            'name': 'JSON CRACK',
            'introduction': 'JSON数据可视化工具，支持放大/缩小、展开/收缩、搜索节点、导出图片等操作。'
        },
        {
            'url': 'https://zhimap.com/',
            'image': 'user/images/zhimap.png',
            'name': 'ZhiMap思维导图',
            'introduction': '一款在线思维导图工具，可以帮助用户创建、编辑和分享思维导图。'
        },
        {
            'url': 'https://www.cnblogs.com/xiaoweigege/p/14954648.html',
            'image': 'user/images/hook.ico',
            'name': 'js-Hook代码',
            'introduction': '常见的js-hook代码合集。'
        },
        {
            'url': 'https://www.runoob.com',
            'image': 'user/images/cainiao.ico',
            'name': '菜鸟教程',
            'introduction': '提供了编程的基础技术教程, 介绍了HTML、CSS、Javascript、Python，Java，Ruby，C，PHP , MySQL等各种编程语言的基础知识。'
        },
    ]
    lapping_tools = [
        {
            'url': 'curl',
            'image': 'user/images/Converters.png',
            'name': 'curl转化器',
            'introduction': 'curl命令转换为requests代码。'
        },
        {
            'url': 'josnformat',
            'image': 'user/images/json.png',
            'name': 'JSON格式化.',
            'introduction': '对无序、压缩的json进行格式化。'
        },
    ]
    return render(request, 'toollist.html', {'online_tools': online_tools, 'lapping_tools': lapping_tools})


def Josnformat(request):
    return render(request, 'josnformat.html')


def getweather(request):
    api_key = 'SI6HZpcDNR58IGe8a'
    location = my_ip
    hours_url = f'https://api.seniverse.com/v3/weather/hourly.json?key={api_key}&location={location}&language=zh-Hans&unit=c&start=0&hours=24'
    days_url = f'https://api.seniverse.com/v3/weather/daily.json?key={api_key}&location={location}&language=zh-Hans&unit=c&start=0&days=7'
    res1 = requests.get(hours_url)
    hours_data = res1.json()['results']
    res2 = requests.get(days_url)
    days_data = res2.json()['results'][0]['daily']

    return JsonResponse({'hours_data': hours_data, 'days_data': days_data})
