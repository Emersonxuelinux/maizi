# -*- coding: utf-8 -*-
import urllib
import urlparse
def demo():
    s = urllib.urlopen('http://blog.kamidox.com')
    # print s.read(100)
    # print s.read() # 全部读出来
    # print s.readline() # 只打印一行
    # lines = s.readlines() # 返回一个列表
    # for line in s.readlines(): print line
    # print s.getcode() #获得状态码
    # -----------------------------------------------------------------------------
    msg = s.info() # 返回一个httpmessage对象
    # print dir(msg) # 使用dir函数获得对象所有方法
    # print msg.headers # 是一个列表
    # print msg.items() # 返回一个列表，包含头文件各个字段组成的元组
    # print msg.getheader('Content-Type') #获取头文件中指定字段的值
    # print msg.gettype() # 获取回应文件类型
    # print msg.getheaders() # 需要传入两个参数 
    # print msg.keys()

# ------------------------urllib.urlretrieve方式:用于获取文件
def retrieve():
    # 从第一个参数开始获取文件，以第二个参数为保存路径
    # python简洁写法，右边本来就要返回一个元组，包含两个值
    # 然后左边两个参数就是元组解包
    fname,msg = \
    urllib.urlretrieve('http://blog.kamidox.com','index.html', reporthook=progress)
    print fname # 这是文件保存路径
    print msg.items() # msg是httpmessage对象

# --------------------------用reporthook实现下载进度
def progress(block,block_size,total_size):
    print('%d/%d - %0.2f%%' % 
        (block * block_size, total_size, 
        (float)(block * block_size) * 100 / total_size))
    
# --------------------------用urllib进行编码和解码
def urlencode():
    params = {'score' : 100, 'name':'爬虫基础', 'coment': 'very good'}
    qs = urllib.urlencode(params) # 传入字典型参数进行编码
    print qs

def urldecode():
    qs = 'coment=very+good&score=100&name=%E7%88%AC%E8%99%AB%E5%9F%BA%E7%A1%80'
    # print qs
    # print (urlparse.parse_qs(qs))
    url =\
    'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E5%A6%82%E4%BD%95%E9%94%BB%E7%82%BC%E6%AF%94%E8%BE%83%E5%A5%BD&rsv_pq=9d6509f2005ab761&rsv_t=b583CVjrEYETPx89UY0AtoqtiOQA5H31RBW6rI%2FbrNqKB92ovD9pYKddzZ0&rqlang=cn&rsv_enter=1&rsv_sug3=22&rsv_sug1=23&rsv_sug7=100'
    result = urlparse.urlparse(url)
    print result # 返回一个parseresult对象
    params = urlparse.parse_qs(result.query)
    print params # 返回一个字典对象

if __name__=='__main__':
    urldecode()
