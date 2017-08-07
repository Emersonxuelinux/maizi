# -*- coding: utf-8 -*-
import time
import scrapy
from scrapy.http import Request

class Example2Spider(scrapy.Spider):
    name = "example2"
   # allowed_domains = ["cn.bing.com", "baidu.com"]
    start_urls = (
        'http://www.baidu.com',
    )

    def parse_further(self, response):
        print response.url

    def parse(self, response):
        for i in range(10, 20):
            yield Request(response.url + ("/s?wd=%d-example2" % i), callback = self.parse_further)
