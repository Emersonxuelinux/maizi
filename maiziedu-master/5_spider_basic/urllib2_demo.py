# -*- coding:utf-8 -*-
'''
urllib2比urllib多了urllib2.Request对象，请求头定制更加丰富
urllib独有编码解码功能
'''
import urllib2
import urllib # 这里主要为了用它进行编码
import cookielib

def urlopen():
    url = 'http://blog.kamidox.com/no_exist'
    try:
        s = urllib2.urlopen(url, timeout=3)
    except urllib2.HTTPError,e:
        print e
    else:
        print s.read(100)
        s.close()

def request():
    # 定制 HTTP 头
    headers = {'User-Agent': 'Mozilla/5.0','x-my-header': 'my value'}
    req = urllib2.Request('http://blog.kamidox.com',headers=headers)
    # urlopen既可以接受网址为参数，也可以接受request对象为参数，后者可以定制请求头
    s = urllib2.urlopen(req)
    print s.read(100)
    print s.headers # 打印回应头的全部信息
    s.close()

def request_post_debug():
    # POST
    data = {'username': 'kamidox', 'password': 'xxxxxxxx'}
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(
        'http://www.douban.com',
        data=urllib.urlencode(data),
                    headers=headers)
    # 自定义handler，这是urllib2的特色。调试等级为1，会打印与服务器交互的信息
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
    s = opener.open(req)
    print s.read(100)
    s.close()

def install_debug_handler():
    opener = urllib2.build_opener(
        urllib2.HTTPHandler(debuglevel=1),
        urllib2.HTTPSHandler(debuglevel=1))
    urllib2.install_opener(opener) # 把自定义的handler安装成默认

def handle_cookie():
    cookiejar = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookiejar=cookiejar)
    opener = urllib2.build_opener(handler,urllib2.HTTPHandler(debuglevel=1))
    # 第一个请求不带cookie
    s = opener.open('https://www.douban.com')
    print(s.read(400))
    s.close()

    # 把获取的cookiex信息打印出来
    print '=' * 80
    print cookiejar._cookies
    print '=' * 80
    # 第二个请求自动把获得的cookie自动加入
    s = opener.open('https://www.douban.com')
    s.close()
if __name__ == '__main__':
    handle_cookie()
