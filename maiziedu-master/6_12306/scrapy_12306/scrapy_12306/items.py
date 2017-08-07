# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ProvinceItem(scrapy.Item):
    name = scrapy.Field()    

class AgencyItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    address = scrapy.Field()
    name = scrapy.Field()
    windows = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()

class StationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bureau = scrapy.Field()
    station = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    passenger = scrapy.Field()
    luggage = scrapy.Field()
    package = scrapy.Field()

class BriefItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    train_no = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    turn = scrapy.Field()

class InfoItem(scrapy.Item):
    train_no = scrapy.Field()
    no = scrapy.Field()
    station = scrapy.Field()
    start_time = scrapy.Field()
    arrive_time = scrapy.Field()
    stopover_time = scrapy.Field()
    seat_type = scrapy.Field()
    turn = scrapy.Field() # 这是

class BriefDeltaItem(scrapy.Item):
    code = scrapy.Field()
    seat_type = scrapy.Field()

class StationCodeItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()

class TicketItem(scrapy.Item):
    train_no = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    swz = scrapy.Field()
    tz = scrapy.Field()
    zy = scrapy.Field()
    ze = scrapy.Field()
    gr = scrapy.Field()
    rw = scrapy.Field()
    yw = scrapy.Field()
    rz = scrapy.Field()
    yz = scrapy.Field()
    wz = scrapy.Field()
    qt = scrapy.Field()
# 这是新添加的，为了更好的量化抓取时间，把多行数据关联在一起
# 其他item也加入相关字段
class TurnItem(scrapy.Item):
    id = scrapy.Field()
    mark = scrapy.Field()
# 这个item设计的非常巧妙，不需要字段
# 它的存在从名字就看出来了
# 类似于信号
# 通知pipeline执行提交操作
class CommitItem(scrapy.Item):
    pass
