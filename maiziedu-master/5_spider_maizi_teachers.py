'''
完成抓取麦子学院老师介绍的任务（只抓取姓名和介绍，不抓图片），并将抓取到的内容保存到文件中进行保存。
抓取地址：
http://www.maiziedu.com/course/teachers/
'''
import urllib.request
import re
import os
from pip.download import user_agent

class Spider(object):
    def __init__(self):
        self.url = 'http://www.maiziedu.com/course/teachers/?page=%s'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'
    def get_page(self,page_index):
        try:
            req = urllib.request.Request(self.url%str(page_index))
            req.add_header('User-Agent',self.user_agent)
            response = urllib.request.urlopen(req)
            content = response.read().decode('utf-8')
            return content
        except urllib.error.HTTPError as e:
            print (e)
            exit()
        except urllib.error.URLError as e:
            print (e)
            exit()
    def parse(self,content):
        pattern_li = re.compile('(?<=<li\ class="t3out">)[\w\W]*?(?=</li>)',re.S)
        items = re.findall(pattern_li,content)
        return items
    def save(self,items,path):
        pattern_title = re.compile('(?<=title=").*?(?=")')
        pattern_intro = re.compile('(?<=简介：</span>).*?(?=</p>)')
        if not os.path.exists(path):
            os.mkdir(path)
        file_path=path+'/teachers.txt'
        f = open(file_path,'a') 
        for item in items:
            title = re.findall(pattern_title,item)
            intro = re.findall(pattern_intro,item)
            f.write(''.join(title)+':'+''.join(intro)+'\n')
        f.close()
    def run(self):
        print('开始抓取内容了...')
        for i in range(1,24):
            content = self.get_page(i)
            items = self.parse(content)
            self.save(items,'maizi_teachers')
        print('好累,终于抓完了...')
if __name__ == '__main__':
    spider = Spider()
    spider.run()


