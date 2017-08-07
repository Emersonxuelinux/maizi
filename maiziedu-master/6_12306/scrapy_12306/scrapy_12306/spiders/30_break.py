# -*- coding: utf-8 -*-
import scrapy
import json

from scrapy.http.request import Request

class BreakSpider(scrapy.Spider):
    name = 'breakpoint'
#    start_urls = ['https://kyfw.12306.cn/otn/userCommon/allProvince']

    def start_requests(self):
        self.logger.info("------------ start request")
        yield Request(url="https://www.baidu.com/s?wd=1")

    def parse_e(self, response):
        self.logger.info(response.url)
        yield Request(url=(response.url + "_1"), callback = self.parse_e)

    def parse(self, response):
        self.logger.info("--------------------------")

        yield Request(url='https://www.baidu.com/s?wd=1', callback = self.parse_e)
        yield Request(url='https://www.baidu.com/s?wd=3', callback = self.parse_e)
        yield Request(url='https://www.baidu.com/s?wd=4', callback = self.parse_e)
        yield Request(url='https://www.baidu.com/s?wd=5', callback = self.parse_e)

