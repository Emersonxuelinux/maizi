# -*- coding: utf-8 -*-
import datetime

from scrapy.exceptions import IgnoreRequest

class DownloaderMiddleware(object):

    def process_request(self, request, spider):
        # 通过turn来作为过时标准
        if "turn" in request.meta:
            turn = request.meta["turn"]
            if turn != spider.turn:
                spider.logger.warning("in midderware, " + request.url +\
                        (" expire. %d %d" % (spider.turn, turn)))
                raise IgnoreRequest()
            else:
                return None

        else:
            return None
