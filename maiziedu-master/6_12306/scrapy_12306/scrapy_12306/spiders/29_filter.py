# -*- coding: utf-8 -*-
import scrapy
import json

from scrapy.http.request import Request

class FilterSpider(scrapy.Spider):
    name = 'filter'
    start_urls = ['https://www.baidu.com/s?wd=22']

    def parse_e(self, response):
        self.logger.info(response.url)
        yield Request(url=response.url, callback = self.parse_e)

    def parse(self, response):
        self.logger.info("--------------------------")
        # DEBUG: Filtered duplicate request
        yield Request(url='https://www.baidu.com/s?wd=3', callback = self.parse_e)
        yield Request(url='https://www.baidu.com/s?wd=3', callback = self.parse_e)

