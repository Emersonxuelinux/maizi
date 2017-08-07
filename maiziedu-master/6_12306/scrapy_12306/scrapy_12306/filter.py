# -*- coding: utf-8 -*-

#import hashlib

from scrapy.dupefilters import RFPDupeFilter

import logging

logger = logging.getLogger()

class URLTurnFilter(RFPDupeFilter):
    def request_fingerprint(self, request):
#        logger.info("fliter " + request.url)
        # 以turn作为去重标准之一
        # 也就是说，如果是同一轮的同一请求就过滤去重
        if "turn" in request.meta:
            return request.url + ("-- %d" % request.meta["turn"])
        else:
            return request.url














# vim: set ts=4 sw=4 sts=4 tw=100 et:
