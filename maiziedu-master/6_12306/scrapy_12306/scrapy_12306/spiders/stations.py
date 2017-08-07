# -*- coding: utf-8 -*-
import json
import urllib

import scrapy
from scrapy.http.request import Request
from scrapy_12306.items import StationItem
from scrapy_12306.items import CommitItem

class StationsSpider(scrapy.Spider):
    name = 'StationsSpider'
    start_urls = ['http://www.12306.cn/mormhweb/kyyyz/']

    custom_settings = {
            'ITEM_PIPELINES': {
                'scrapy_12306.pipelines.StationSQLPipeline': 300,
            },
    }

    def parse(self, response):
        # css选择器就是chrome中复制selector那个
        # 返回一个选择器，extract后返回字符串，是unicode编码
        names = response.css("#secTable > tbody > tr > td::text").extract()
        sub_urls = response.css("#mainTable td.submenu_bg > a::attr(href)").extract()
        # 第一次请求站点页面之后再根据抓取的站点名称分别发出数据请求
        # 第二次请求响应的是站点数据
        for i in range(0, len(names)):
            # 偶数为车站数据
            sub_url1 = response.url + sub_urls[i * 2][2:]
            # meta是一个字典，声明是否为站点
            yield Request(sub_url1, callback = self.parse_station, meta = {'bureau':names[i], 'station':True})
            # 奇数为乘降所数据
            sub_url2 = response.url + sub_urls[i * 2 + 1][2:]
            yield Request(sub_url2, callback = self.parse_station, meta = {'bureau':names[i], 'station':False})
    # 对第二次请求得到的响应进行解析
    def parse_station(self, response):
        datas = response.css("table table tr")
        # 这个结果很容易出错，所以调试时要特别关注，用debug
        self.logger.debug(datas)
        # critical: 
        # error: 比较严重的错误，恢复可能性比较小
        # warning: 程序出错时使用，比较小的错误，比如网络中断，但是如果持续出错就需要修改
        # info: 程序运行时比较关注的信息，比如发出顺序
        # debug: 调试时使用，正式运行之后要关闭
        if len(datas) <= 2:
            self.logger.info('no item ' + response.meta["bureau"] + ' ' + response.meta["station"])
            return
        for i in range(0, len(datas)):
            if i < 2:
                continue
            infos = datas[i].css("td::text").extract()

            item = StationItem()
            # 专门有字段确定是否为站点
            item["bureau"] = response.meta["bureau"]
            item["station"] = response.meta["station"]
            item["name"] = infos[0]
            item["address"] = infos[1]
            # 如果不为中文空，代表打上了勾
            item["passenger"] = infos[2].strip() != u""
            item["luggage"] = infos[3].strip() != u""
            item["package"] = infos[4].strip() != u""
            yield item
        yield CommitItem()



