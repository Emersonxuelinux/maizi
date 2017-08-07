# -*- coding: utf-8 -*-
import requests
import re
from HTMLParser import HTMLParser


def _attr(attrs, attrname):
    for attr in attrs:
        if attr[0] == attrname:
            return attr[1]
    return None


class PoemParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        # 默认未进入特定的标签，后面如果找到符合条件的标签再改为True,然后开始抓取
        self.in_div = False
        self.in_a = False
        # 用compile方便后面复用正则表达式，为了提高可读性，还可以用注释模式
        self.pattern = re.compile(r'''
            (.*)  # 匹配标题  group(1)
            \(  # 匹配作者左边的括号
            (.*)  # 匹配作者  group(2)
            \)  # 匹配作者右表的括号
            ''', re.VERBOSE)
        self.tangshi_list = []
        self.current_poem = {}
        pass

    def handle_starttag(self, tag, attrs):
        # 如果找到目标标签内容，就把标志改为True
        if tag == 'div' and _attr(attrs, 'class') == 'guwencont2':
            self.in_div = True

        if tag == 'a' and self.in_div:
            self.in_a = True
            self.current_poem['url'] = _attr(attrs, 'href')

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.in_a:
            print(data)
            # 调用定义好的compile对象进行提取
            m = self.pattern.match(data)
            if m:  # 如果取到了数据，就直接把分组正则获取的内容放入当前正在抓取的古诗
                self.current_poem['title'] = m.group(1)
                self.current_poem['author'] = m.group(2)
                self.tangshi_list.append(self.current_poem)
                # 每次保存之后需要初始化，避免被覆盖，只抓取同一首
                self.current_poem = {}


def retrive_tangshi_300():
    url = 'http://www.gushiwen.org/gushi/tangshi.aspx'
    r = requests.get(url)
    # 专门解析唐诗的解析器
    parser = PoemParser()
    parser.feed(r.content)
    return parser.tangshi_list


if __name__ == '__main__':
    l = retrive_tangshi_300()
    print('total %d poems.' % len(l))
    for i in range(10):
        print('标题: %(title)s\t作者：%(author)s\tURL: %(url)s' % (l[i]))

