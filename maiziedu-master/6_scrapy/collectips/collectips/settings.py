# -*- coding: utf-8 -*-

# Scrapy settings for collectips project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'collectips'

SPIDER_MODULES = ['collectips.spiders']
NEWSPIDER_MODULE = 'collectips.spiders'

# 用于连接数据库的参数
DBKWARGS={'db':'test','user':'root', 'passwd':'123456',
    'host':'localhost','use_unicode':True, 'charset':'utf8'}


# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# 配置启用刚才写的pipeline
ITEM_PIPELINES = {
   'collectips.pipelines.CollectipsPipeline': 300,
}

#Configure log file name
# 配置log文件
LOG_FILE = "scrapy.log"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# 设置客户端信息
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0'

