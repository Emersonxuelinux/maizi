# -*- coding: utf-8 -*-

# Scrapy settings for topgoods project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'topgoods'

SPIDER_MODULES = ['topgoods.spiders']
NEWSPIDER_MODULE = 'topgoods.spiders'
# 打开下载中间件
#DOWNLOADER_MIDDLEWARES = {
#        'scrapy.downloadermiddleware.httpproxy.HttpProxyMiddleware':301,
 #   }
# 打开图片下载管道
ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}
# 把items中的图片链接字段配置在这里
IMAGES_URLS_FIELD = 'file_urls'
# 设置图片保存路径,这个字段存的是原尺寸
IMAGES_STORE = r'.'
# 另外可以设置缩略图文件夹
# 花括号里的字符串可以自定义，表示文件路径，然后带上图片尺寸
IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}
LOG_FILE = "scrapy.log"
