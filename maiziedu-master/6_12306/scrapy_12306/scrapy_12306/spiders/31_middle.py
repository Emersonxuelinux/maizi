# -*- coding: utf-8 -*-
import json
import time
import datetime

import scrapy

from scrapy.http.request import Request

class MiddleSpider(scrapy.Spider):
    name = 'middle'

    custom_settings = {
            'DUPEFILTER_DEBUG': True,
            'DOWNLOADER_MIDDLEWARES': {
                'scrapy_12306.custom_middle.CustomDownloaderMiddleware': 500
                }
    }

    def start_requests(self):
        self.logger.info("------------ start requests")
        yield Request(url="https://www.baidu.com/s?wd=20")

    def parse_e(self, response):
        self.logger.info("------------ response")

        self.logger.info(response.url)
        yield Request(url='https://www.baidu.com/s?wd=1', callback = self.parse_e, meta = {"expire":response.meta["expire"]})
#        yield Request(url=(response.url + "_1"), callback = self.parse_e)

    def parse(self, response):
        self.logger.info("------------ response 4 start")

        yield Request(url='https://www.baidu.com/s?wd=2', callback = self.parse_e, meta = {"expire":datetime.datetime.now() + datetime.timedelta(seconds = 2)})
        yield Request(url='https://www.baidu.com/s?wd=3', callback = self.parse_e, meta = {"expire":datetime.datetime.now() + datetime.timedelta(seconds = 2)})
        yield Request(url='https://www.baidu.com/s?wd=4', callback = self.parse_e, meta = {"expire":datetime.datetime.now() + datetime.timedelta(seconds = 2)})
