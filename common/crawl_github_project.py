from curl_cffi import requests
from parsel import Selector
from loguru import logger

from tools.models import ProjectCase


def crawl_project_case():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    }
    try:
        proxies = {'http': 'socks5://127.0.0.1:42004', 'https': 'socks5://127.0.0.1:42004'}
        response = requests.get('https://github.com/trending/', headers=headers, impersonate='chrome110', proxies=proxies)
    except:
        proxies = {'http': 'socks5://192.168.1.171:1080', 'https': 'socks5://192.168.1.171:1080'}
        response = requests.get('https://github.com/trending/', headers=headers, impersonate='chrome110', proxies=proxies)
    ProjectCase.objects.all().delete()
    sel = Selector(response.text)
    article_list = sel.xpath('//article')
    for article in article_list:
        name = article.xpath('./h2/a/@href').get(default='').strip()
        describe = article.xpath('./p//text()').get(default='').strip()
        language = article.xpath('.//span[@itemprop="programmingLanguage"]/text()').get(default='').strip()
        starts = article.xpath(".//a[contains(@href,'stargazers')]/text()").get(default='').strip()
        forks = article.xpath(".//a[contains(@href,'forks')]/text()").get(default='').strip()
        my_dict = {
            'name': name,
            'describe': describe,
            'language': language,
            'starts': starts,
            'forks': forks,
            'date_range': 'day',
        }
        logger.info(my_dict)
        ProjectCase.objects.create(**my_dict)