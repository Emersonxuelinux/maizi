# -*- coding: utf-8 -*-
import datetime

from scrapy.exceptions import IgnoreRequest
# 对断点续传间隔时间过长也可以处理
class CustomDownloaderMiddleware(object):

    def process_request(self, request, spider):
        # 先打印日志，方便分析
        spider.logger.info("in midderware, " + request.url)
        # 对expire值进行处理
        if "expire" in request.meta:
            s1 = request.meta["expire"]
            s2 = datetime.datetime.now()
            # 如果超过了过期时间，就认为过期而丢弃请求
            if s1 < s2:
                spider.logger.warning("in midderware, " + request.url + " expire.")
                raise IgnoreRequest()
            # 如果没有过期，就不处理
            else:
                return None

        else:
            spider.logger.info("in midderware, don't deal")
            return None

















# vim: set ts=4 sw=4 sts=4 tw=100 et:
