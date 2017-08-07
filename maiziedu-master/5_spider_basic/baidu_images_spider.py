# -*- coding: utf-8 -*-
import requests
import urllib
import os
import threading
import datetime


# 保存所有待操作的url
gImageList = []
gCondition = threading.Condition()


# 主要把图片url放入待下载列表gImageList
class Producer(threading.Thread):
    def run(self):
        global gImageList
        global gCondition

        print('%s started' % threading.current_thread())
        imgs = download_wallpaper_list()

        gCondition.acquire()
        for img in imgs:
            if 'downloadUrl' in img:
                gImageList.append(img['downloadUrl'])
        print('%s: produced %d urls. Left %d urls.' % (threading.current_thread(), len(imgs) - 1, len(gImageList)))
        gCondition.notify_all()
        gCondition.release()

# 从gImageList中取出图片url下载
class Consumer(threading.Thread):

    def __init__(self, folder='wallpaper', group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Consumer, self).__init__(group, target, name, args, kwargs, verbose)
        self.folder = folder

    def run(self):
        global gImageList
        global gCondition

        print('%s started' % threading.current_thread())
        while True:
            gCondition.acquire()
            print('%s: trying to download image. Queue length is %d' % (threading.current_thread(), len(gImageList)))
            while len(gImageList) == 0:
                gCondition.wait()
                print('%s: waken up. Queue length is %d' % (threading.current_thread(), len(gImageList)))
            url = gImageList.pop()
            gCondition.release()
            # 只对不支持并发的函数才用锁保护，这样才能提高程序的并发性
            _download_image(url, self.folder)


def _download_image(url, folder):
    # 如果不存在就创建它
    if not os.path.isdir(folder):
        os.mkdir(folder)

    print('downloading %s' % url)
    # 用匿名函数获取url中最后一段字符作为文件名
    _filename = lambda s: os.path.join(folder, os.path.split(url)[1])
    r = requests.get(url)
    with open(_filename(url), 'wb') as f:
        f.write(r.content)
    return _filename(url)


def download_wallpaper_list():
    # 数据分析
    # http://image.baidu.com/channel/wallpaper#%E7%83%AD%E9%97%A8%E6%8E%A8%E8%8D%90&%E5%85%A8%E9%83%A8&6&0
    # 分析得知只要往这个url发送带数据的请求，就会返回一个json文件
    url = 'http://image.baidu.com/data/imgs'
    # 用chrome分析得出需要发送的数据
    params = {
        'pn': 41,
        'rn': 100,
        'col': '壁纸',
        'tag': '国家地理',
        'tag3': '',
        'width': 1600,
        'height': 900,
        'ic': 0,
        'ie': 'utf8',
        'oe': 'utf-8',
        'image_id': '',
        'fr': 'channel',
        'p': 'channel',
        'from': 1,
        'app': 'img.browse.channel.wallpaper',
        't': '0.016929891658946872'
    }
    s = requests.get(url, params=params)
    # 用json解析
    imgs = s.json()['imgs']
    print('%s: totally %d images' % (threading.current_thread(), len(imgs)))
    return imgs


if __name__ == '__main__':
    # download_wallpaper()
    Producer().start()

    for i in range(2):
        Consumer(folder='wallpaper').start()



