# -*- coding: utf-8 -*-

#import hashlib

from scrapy.dupefilters import RFPDupeFilter
# 通过查看源码知道只要继承RFPDupeFilter这个类就可以控制去重
class CustomURLFilter(RFPDupeFilter):
    # 这是生成指纹的方法，用来控制辨别重复的标准
    def request_fingerprint(self, request):
        # 这里是以时间戳生成指纹
        if "timestamp" in request.meta:
            return request.url + "--" + request.meta["timestamp"]
        else:
            return request.url

