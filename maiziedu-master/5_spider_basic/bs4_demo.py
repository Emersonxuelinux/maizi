# -*- coding: utf-8 -*-
'''
http://quote.eastmoney.com/stocklist.html
官方文档：http://beautifulsoup.readthedocs.io/zh_CN/latest/
'''
from bs4 import BeautifulSoup
import re
import urllib2


def get_html(url):
    response = urllib2.urlopen(url)
    return response.read()


def get_content(content):
    results = []
    # 获取股票代码
    reobj1 = re.compile(r'.*?\((\d+)\)')
    # 获取股票名称
    reobj2 = re.compile(r'(.*?)\(.*?\)')

    bs = BeautifulSoup(content)
    # 找到所有指定id的div
    lis = bs.find_all('div', id="quotesearch")
    # 在第一个div中找第一个ul
    ul = lis[0].find('ul')
    # 获取所有li标签
    son_lis = ul.find_all('li')
    for li in son_lis:
        text = li.text
        code = reobj1.findall(text)[0]
        sname = reobj2.findall(text)[0]
        results.append((code, sname))
    return results


if __name__ == "__main__":
    url = 'http://quote.eastmoney.com/stocklist.html'
    html = get_html(url)
    rs = get_content(html)
    for x, y in rs:
        print x, "--", y
