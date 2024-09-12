import subprocess

curl_command = """
curl 'http://192.168.1.186:8000/proxypool/proxylist/' \
  -H 'Connection: keep-alive' \
  -H 'Cache-Control: max-age=0' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.244.400 QQBrowser/12.5.5646.400' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'Referer: http://192.168.1.186:8000/tools/curl/' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Cookie: csrftoken=OmFOVOlii6pMtFycRfUtVqeo0QuvcaoX; sessionid=87am9gdgp7lli7c68x23boz6aafharpi' \
  --compressed \
  --insecure
"""

import re


def is_curl_command(command):
    # 定义一些典型的 curl 命令选项
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

print(is_curl_command(curl_command))