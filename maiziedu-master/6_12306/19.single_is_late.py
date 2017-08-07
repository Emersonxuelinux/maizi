# -*- coding: utf-8 -*-

import time
import datetime
import json

import urllib
import requests

def fetch_schedule(train_code, station_name, depart):
    url = "http://dynamic.12306.cn/map_zwdcx/cx.jsp"

    params = {"cz" : station_name, "cc" : train_code,
            "cxlx" : "1" if depart else "0",
            "rq" : datetime.datetime.now().strftime("%Y-%m-%d"),
            "czEn" : urllib.quote(station_name.encode("utf-8")).replace("%", "-"),
            "tp": int(time.time() * 1000)}
    # 没有headers就会被拒绝访问
    headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"}

    try:
        s = requests.get(url, params = params, headers = headers)
    except Exception, e:
        print "request fail. " + url
        raise e


    print s.content.strip().decode("gbk").encode("utf-8")

if __name__ == "__main__":
    fetch_schedule("D354", u"常州", False)
















# vim: set ts=4 sw=4 sts=4 tw=100 et:
