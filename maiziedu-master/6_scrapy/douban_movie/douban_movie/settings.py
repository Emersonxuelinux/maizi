# -*- coding: utf-8 -*-

BOT_NAME = 'douban_movie'

SPIDER_MODULES = ['douban_movie.spiders']
NEWSPIDER_MODULE = 'douban_movie.spiders'


# 打开图片下载管道
ITEM_PIPELINES = {
    'douban_movie.pipelines.MyImagesPipeline': 300,
    'douban_movie.pipelines.IntroPipeline': 500,
    }
# 把items中的图片链接字段配置在这里
IMAGES_URLS_FIELD = 'post_urls'
# 设置图片保存路径
IMAGES_STORE = r'.'


LOG_FILE = "scrapy.log"