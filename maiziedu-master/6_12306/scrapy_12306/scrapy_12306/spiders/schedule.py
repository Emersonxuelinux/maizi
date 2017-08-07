# -*- coding: utf-8 -*-
import time
import datetime
import json
import urllib

import scrapy
from scrapy.http.request import Request
from scrapy_12306.items import BriefItem
from scrapy_12306.items import InfoItem
from scrapy_12306.items import TurnItem
from scrapy_12306.items import CommitItem

class ScheduleSpider(scrapy.Spider):
    name = 'ScheduleSpider'
    # 这个只能用于固定的简单链接
    #start_urls = ['https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName']

    custom_settings = {
            'ITEM_PIPELINES': {
                'scrapy_12306.pipelines.Schedule_SQLPipeline': 300,
            },
            'DUPEFILTER_DEBUG': True,
            'DOWNLOADER_MIDDLEWARES': {
                'scrapy_12306.middle.DownloaderMiddleware': 500,
            },
            'DUPEFILTER_CLASS': "scrapy_12306.filter.URLTurnFilter",
    }
    # 在构造方法中初始化这次爬取的轮次
    def __init__(self, *a, **kw):
        super(ScheduleSpider, self).__init__(*a, **kw)
        # 24小时为一轮
        # 24小时之内抓取的都算一轮
        turn = int(time.time() / 86400)
        self.turn = turn
#        self.turn = 1
        self.logger.info("this turn %d" % turn)

    # 如果是比较复杂的动态链接，就用start_requests代替start_urls
    def start_requests(self):
        self.logger.info("-------------------------")

        turnItem = TurnItem()
        turnItem["id"] = self.turn
        turnItem["mark"] = n.strftime("%Y-%m-%d %H:%M:%S")

        url = "https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?"
        # 这里实现了根据当前时间发起的http请求
        t = (datetime.datetime.now() + datetime.timedelta(days = 3)).strftime("%Y-%m-%d")
        params = {"date":t}
        # 使用urllib对带参数的url进行编码
        s_url = url + urllib.urlencode(params)
        self.logger.debug("start url " + s_url)
        # 最后返回一个构造好的请求
        # 带参数并编码好的url
        # 回调函数
        # 用meta传送变量值到回调函数
        # 添加轮次信息，方便中间件过滤
        yield Request(s_url, callback = self.parse, meta = {"t":t, "turn":self.turn, "item":turnItem})

    def parse(self, response):
        yield response.meta["item"]
        # 获取的response.body就是json格式的
        datas = json.loads(response.body)
        url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?"
        for data in datas["data"]:
            item = BriefItem() 
            briefs = data["station_train_code"].split("(")
            item["train_no"] = data["train_no"]
            item["code"] = briefs[0]
            briefs = briefs[1].split("-")
            item["start"] = briefs[0]
            item["end"] = briefs[1][:-1]
            yield item
            # 根据获取数据构造url要传递的参数
            params = u"train_no=" + data["train_no"] + u"&from_station_telecode=BBB&to_station_telecode=BBB&depart_date=" + response.meta["t"]
            # 这是第二次请求了，同样有url，callback，meta传递
            yield Request(url + params, callback = self.parse_train_schedule, meta = {"train_no":data["train_no"]})
    # 第二级请求获得的响应才是时刻表
    def parse_train_schedule(self, response):
        stations = json.loads(response.body)

        datas = stations["data"]["data"]
        size = len(datas)
        for i in range(0, size):
            data = datas[i]

            info = InfoItem()
            info["train_no"] = response.meta["train_no"];
            info["no"] = int(data["station_no"])
            info["station"] = data["station_name"]
            info["turn"] = response.meta["turn"]

            if data["start_time"] != u"----":
                info["start_time"] = data["start_time"] + u":00";
            else:
                info["start_time"] = None

            if data["arrive_time"] != u"----":
                info["arrive_time"] = data["arrive_time"] + u":00";
            else:
                info["arrive_time"] = None

            if data["stopover_time"] != u"----":
                info["stopover_time"] = data["stopover_time"] + u":00";
            else:
                info["stopover_time"] = None

            yield info
        yield CommitItem()
          



