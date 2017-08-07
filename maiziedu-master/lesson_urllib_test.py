#! /maizi_env/bin/env python3
#coding:utf-8
'''
课程http与urllib2的演示例子
'''
#python2 版本
'''
import urllib2
if __name__=='__main__':
    url = "http://www.baidu.com"
    #设置头部信息，否则有些网站会进行限制
    headers = {'User-Agent': ...}
    request = urllib2.Request(url=url,headers=headers)
    response = urllib2.urlopen(request)
    print (response.read())
'''

#python3 版本
'''
urllib2在Python3已拆分更名为urllib.request和urllib.error
'''
import urllib.request

if __name__=='__main__':
    url = "http://www.baidu.com"
    response = urllib.request.urlopen(url)
    print (response.read())
