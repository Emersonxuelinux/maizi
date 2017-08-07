# -*- coding:utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import pdb

title = []
class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # print item['title']
        global title
        title = item['title']
        for image_url in item['post_urls']:
            yield Request(image_url)
    # 这里的request就是图片链接请求
    def file_path(self, request, response=None, info= None):
        # print '这里执行的是file_path'
        global title
        # image_guid = request.url.split('/')[-1]
        return 'full/%s/%s' % (title, title+'.jpg')
    # 这里的路径值来自于file_path
    # 这里最后返回item
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item 

class IntroPipeline(object):
    def process_item(self, item, spider):
        # pdb.set_trace()
        intro = item['intro']
        title = item['title']
        intro_path = 'full/%s/%s.txt' % (title, title)
        with open(intro_path, 'w+') as file:
            file.write(intro)
        return item