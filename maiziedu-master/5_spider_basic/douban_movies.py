# -*- coding: utf-8 -*-
'''
使用时需要定义一个从类HTMLParser继承的类，重定义函数：
handle_starttag( tag, attrs)
handle_startendtag( tag, attrs)
handle_endtag( tag)

来实现自己需要的功能。

tag是的html标签，attrs是 (属性，值)元组(tuple)组成的列表(list)。
HTMLParser自动将tag和attrs都转为小写。
'''



'''
HTMLParser是python用来解 析html的模块。它可以分析出html里面的标签、数据等等，是一种处理html的简便途径。 HTMLParser采用的是一种事件驱动的模式，当HTMLParser找到一个特定的标记时，它会去调用一个用户定义的函数，以此来通知程序处理。它主要的用户回调函数的命名都是以handler_开头的，都是HTMLParser的成员函数。当我们使用时，就从HTMLParser派生出新的类，然后重新定义这几个以handler_开头的函数即可。这几个函数包括：
handle_startendtag 处理开始标签和结束标签
handle_starttag 处理开始标签，比如<xx>
handle_endtag 处理结束标签，比如</xx>
handle_charref 处理特殊字符串，就是以&#开头的，一般是内码表示的字符
handle_entityref 处理一些特殊字符，以&开头的，比如  
handle_data 处理数据，就是<xx>data</xx>中间的那些数据
handle_comment 处理注释
handle_decl 处理<!开头的，比如<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
handle_pi 处理形如<?instruction>的东西
'''
import urllib2
from HTMLParser import HTMLParser


class MovieParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies = []
    # 重写这个方法来处理开始标签标签,因为这些要取的属性值都写在<li>中
    # 这个方法中的tag指<li>这种标签，attrs指相关属性值，二者已经写好了处理逻辑会自动整理好传入
    def handle_starttag(self,tag,attrs):
        # 定义一个内部函数用来解析属性
        def _attr(attrlist, attrname):  # 传入属性列表和要获取属性值的属性名
            for attr in attrlist:  # 取出的attr是元组，0下标指属性名，1下标指向属性值
                if attr[0] == attrname:
                    return attr[1]
            return None

        # 找到列表标签中data-title属性值不为空和data-category属性值为nowplaying的li标签内容
        if tag == 'li' and _attr(attrs, 'data-title') and _attr(attrs, 'data-category') == 'nowplaying':
            movie = {}
            # 用内部方法把需要的属性值取出来
            movie['title'] = _attr(attrs, 'data-title')
            movie['score'] = _attr(attrs, 'data-score')
            movie['director'] = _attr(attrs, 'data-director')
            movie['actors'] = _attr(attrs, 'data-actors')
            self.movies.append(movie)
            print('%(title)s|%(score)s|%(director)s|%(actors)s' % movie)




def nowplaying_movies(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    req = urllib2.Request(url, headers=headers)
    s = urllib2.urlopen(req)
    parser = MovieParser()  # 这是另外准备好的电影解析器
    parser.feed(s.read())  # 给解析器喂数据
    s.close()
    return parser.movies  # 解析器解析后返回解析好的电影


if __name__ == '__main__':
    url = 'https://movie.douban.com/nowplaying/xiamen/'
    movies = nowplaying_movies(url)

    import json
    # 转换成json格式再打印一次
    print('%s' % json.dumps(
        movies, sort_keys=True, indent=4, separators=(',', ': ')))
