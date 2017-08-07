# -*- coding: utf-8 -*-

# import the spiders you want to run
from spiders.example1 import Example1Spider
from spiders.example2 import Example2Spider

# scrapy api imports
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

crawler = CrawlerProcess(settings)
# 这个修饰方法依赖于twisted
@defer.inlineCallbacks
# 在这里指定爬虫执行顺序
def crawl():
    yield crawler.crawl(Example1Spider)
    yield crawler.crawl(Example2Spider)

crawl()
crawler.start()















# vim: set ts=4 sw=4 sts=4 tw=100 et:
