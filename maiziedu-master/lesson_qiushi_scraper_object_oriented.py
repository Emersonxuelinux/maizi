'''
3.3 重构爬虫代码（三）
'''
import urllib2
import re
import os
from pip.download import user_agent

class Spider(object):
    #抓取过程：
    #1.访问其中一个网页地址，获取网页源代码
    def __init__(self):
        self.url = 'http://www.qiushibaike.com/8hr/page/%s/?s=4873681'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'
    def get_page(self,page_index):   
        headers = {'User-Agent': self.user_agent}
        try:
            request = urllib2.Request(url=self.url%str(page_index),headers=headers)
            response = urllib2.urlopen(request)
            content =  response.read()
            return content
        except urllib2.HTTPError as e:
            print (e)
            exit()
        except urllib2.URLError as e:
            #print (e)
            print ('网络无法访问')
            exit()
    #分析网页源代码
    def analysis(self,content):  
        pattern = re.compile('<div class="content">(.*?).*?<!--(.*?)-->.*?</div>',re.S)
        items = re.findall(pattern,content)
        return items
    #保存抓取的内容       
    def save(self,items,path):
        for item in items:
            #取消多余的换行符\n,再把</br>换成\n
            item_new = item[0].replace('\n','').replace('</br>','\n')
            #3.保存抓取的数据
            path = 'qiubai'
            if not os.path.exists(path):
                os.mkdir(path)
            file_path = path+'/'+item[1]+'.txt'
            f = open(file_path,'w')
            f.write(item_new)
            f.close()
    #运行的方法
    def run(self):
        print ('开始抓取内容了。。。')
        for i in range(1,35):
            content = self.get_page(i)
            items = self.analysis(content)
            self.save(items,'qiubai')
        print ('内容抓取完了')
if __name__ == '__main__':
    spider = Spider()
    spider.run()
