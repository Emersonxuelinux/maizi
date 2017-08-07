'''
先在#后面把步骤写完，然后一步步实现
'''
import urllib2
import re
import os
from pip.download import user_agent
if __name__ == '__main__':
    #抓取过程：
    #1.访问其中一个网页地址，获取网页源代码
    for i in range(1,35):
        url = 'http://www.qiushibaike.com/8hr/page/'+str(i)+'/?s=4873681'
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'
        headers = {'User-Agent': user_agent}
        try:
            request = urllib2.Request(url=url,headers=headers)
            response = urllib2.urlopen(request)
            content =  response.read()
        except urllib2.HTTPError as e:
            print (e)
            exit()
        except urllib2.URLError as e:
            print (e)
            exit()
        print (content)
        #2.根据抓取到的内容提取想要的数据
        pattern = re.compile('<div class="content">(.*?).*?<!--(.*?)-->.*?</div>',re.S)
        print (re.findall(pattern,content))
        for item in items:
            print (item)
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
