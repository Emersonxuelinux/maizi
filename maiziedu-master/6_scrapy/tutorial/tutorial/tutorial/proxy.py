# -*- coding:utf-8 -*-
from selenium import webdriver
from handledb import exec_sql
import socket
import urllib2

# 事先定义好后面要用的数据库参数
dbapi = "MySQLdb"
kwargs = {
    'user': 'root',
    'passwd': '123456',
    'db': 'test',
    'host': 'localhost',
    'use_unicode': True}

def counter(start_at=0):
    '''Function: count number
	Usage: f=counter(i) print f() #i+1'''
    count=[start_at]
    def incr():
        count[0]+=1
        return count[0]
    return incr

# 定义方法使用代理打开链接


def use_proxy(browser, proxy, url):
    '''Open browser with proxy'''
    # 用代理打开浏览器
    # 访问之后就切换代理ip
    # 注意传入的browser其实是selenium的webdriver生成的一个浏览器对象
    # browser = webdriver.Chrome()
    # 先获取浏览器档案
    profile = browser.profile
    # 设置档案代理类型
    profile.set_preference('network.proxy.type', 1)
    # 设置档案http代理
    profile.set_preference('network.proxy.http', proxy[0])
    # 设置代理端口
    profile.set_preference('network.proxy.http_port', int(proxy[1]))
    # 设置网页图像显示
    profile.set_preference('permissions.default.image', 2)
    # 更新档案
    profile.update_preferences()
    browser.profile = profile
    # 用浏览器打开链接
    browser.get(url)
    # 设置超时时间
    browser.implicitly_wait(30)
    return browser

# 这个单例模型用于获取ip的类继承
class Singleton(object):
    '''Signal instance example.'''
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance 

# 这个类用于获取ip


class GetIp(Singleton):
    # 每次创建实例时就自动进行查询获取可用代理ip
    def __init__(self):
        sql = '''SELECT  `IP`,`PORT`,`TYPE`
        FROM  `proxy`
        WHERE `TYPE` REGEXP  'HTTP|HTTPS'
        AND  `SPEED`<5 OR `SPEED` IS NULL
        ORDER BY `proxy`.`TYPE` ASC
        LIMIT 50 '''
        self.result = exec_sql(sql, **kwargs)

    # 把不能用的ip删掉
    def del_ip(self, record):
        '''delete ip that can not use'''
        sql = "delete from proxy where IP='%s' and PORT='%s'" % (record[0], record[1])
        print sql
        exec_sql(sql, **kwargs)
        print record, " was deleted."
    
    # 判断ip是否能用
    def judge_ip(self, record):
        '''Judge IP can use or not'''
        # 先分别对http和https进行处理
        http_url = "http://www.baidu.com/"
        https_url = "https://www.alipay.com/"
        proxy_type = record[2].lower()
        url = http_url if proxy_type == "http" else https_url
        proxy = "%s:%s" % (record[0], record[1])
        # 下面开始判断
        try:  # 首先看是否超时，速度太慢不行
            req = urllib2.Request(url=url)
            req.set_proxy(proxy, proxy_type)
            response = urllib2.urlopen(req, timeout=30)
        except Exception, e:
            print "Request Error:", e
            self.del_ip(record)
            return False
        else:  # 然后看状态码是否正常，能否使用
            code = response.getcode()
            if code >= 200 and code < 300:
                print 'Effective proxy',record
                return True
            else:
                print 'Invalide proxy',record
                self.del_ip(record)
                return False
    # 这是核心方法，这个类就是用来获取可用且高速的代理ip
    def get_ips(self):
        print "Proxy getip was executed."
        # 这两个列表解析式用法很简洁
        # 分别返回高速的http和https可用代理ip
        http = [h[0:2] for h in self.result if h[2] =="HTTP" and self.judge_ip(h)]
        https=[h[0:2] for h in self.result if h[2] =="HTTPS" and self.judge_ip(h)]
        print "Http: ",len(http),"Https: ",len(https)
        return {"http":http,"https":https}