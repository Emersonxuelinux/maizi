# -*- coding: utf-8 -*-
import scrapy
import json

from scrapy.http.request import Request

class CustomSpider(scrapy.Spider):
    name = 'custom_spider'

    start_urls = ['https://kyfw.12306.cn/otn/userCommon/allProvince']
    # 自定义设置中指定使用自定去重类
    custom_settings = {
            'DUPEFILTER_DEBUG': True,
            'DUPEFILTER_CLASS': "scrapy_12306.custom_filter.CustomURLFilter"
    }
    # 发出请求后的回调函数
    # 凡是打印了信息的就是没有去重的
    def parse_e(self, response):
        self.logger.info(response.url)
        self.logger.info(response.meta)

    def parse(self, response):
        self.logger.info("--------------------------")
        j = json.loads(response.body)
        for prov in j["data"]:
            self.logger.info(prov["chineseName"])
        # 前三个没有时间戳，后两个会被去重
        yield Request(url='https://www.baidu.com/s?wd=1', callback = self.parse_e)
        yield Request(url='https://www.baidu.com/s?wd=3', callback = self.parse_e)
        yield Request(url='https://www.baidu.com/s?wd=3', callback = self.parse_e)
        # 后三个有时间戳，后两个会被去重
        yield Request(url='https://www.baidu.com/s?wd=3', callback = self.parse_e, meta = {"timestamp":"1"})
        yield Request(url='https://www.baidu.com/s?wd=3', callback = self.parse_e, meta = {"timestamp":"2"})
        yield Request(url='https://www.baidu.com/s?wd=3', callback = self.parse_e, meta = {"timestamp":"2"})

