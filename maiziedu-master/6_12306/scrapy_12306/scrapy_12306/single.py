# -*- coding: utf-8 -*-

# import the spiders you want to run
from spiders.example1 import Example1Spider

# scrapy api imports
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
# 读取全局配置文件settings.py
settings = get_project_settings()
# 传入上面读取的配置信息
crawler = CrawlerProcess(settings)
# 然后传入要执行的爬虫名
crawler.crawl(Example1Spider)
# 开始爬取
crawler.start()















# vim: set ts=4 sw=4 sts=4 tw=100 et:
