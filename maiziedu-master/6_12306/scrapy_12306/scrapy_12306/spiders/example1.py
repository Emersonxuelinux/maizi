# -*- coding: utf-8 -*-
import time
import scrapy
from scrapy.http import Request

class Example1Spider(scrapy.Spider):
    name = "example1"
   # allowed_domains = ["cn.bing.com", "baidu.com"]
    start_urls = (
        'http://www.baidu.com',
    )

    def parse_further(self, response):
        print response.url

    def parse(self, response):
        for i in range(10):
            yield Request(response.url + ("/s?wd=%d-example1" % i), callback = self.parse_further)
