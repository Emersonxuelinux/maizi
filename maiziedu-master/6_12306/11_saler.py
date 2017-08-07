# -*- coding: utf-8 -*-

import time
import json

import requests
from bs4 import BeautifulSoup

# 这个函数获取所有代售点所在省份
def fetch_provinces():
    # 通过开发者工具发现这个url
    url = "https://kyfw.12306.cn/otn/userCommon/allProvince"

    try:
        # 因为是发送https请求，所以加入verify参数
        s = requests.get(url, verify=False)
    except Exception, e:
        print "fetch provinces. " + url
        raise e

    j = json.loads(s.content)
    return j["data"]

# 拼接取得某个省的所有代售点信息
def fetch_data(url, province, fd):
    try:
        # 发送的请求里带上省份参数，城市和县城的值为空
        s = requests.get(
            url,
            params={"province": province, "city": "", "county": ""},
            verify=False)
    except Exception, e:
        print "requests url fail.", url, province.encode("utf-8")
        return
    # 处理获取的json数据
    datas = json.loads(s.content)
    for data in datas["data"]["datas"]:
        # 注意空格也要加中文的
        out = u""
        out += data["province"]
        out += u" " + data["city"]
        out += u" " + data["county"]
        out += u" " + data["agency_name"]
        out += u" " + data["address"]
        out += u" " + data["windows_quantity"]
        start = data["start_time_am"]
        end = data["stop_time_pm"]
        out += u" " + start[:2] + u":" + start[2:] + u" - " + end[:2] + u":" + end[2:]
        # 打印前编码为utf-8，否则中文乱码
        s = out.encode("utf-8")
        fd.write(s)
        fd.write("\n")
        print s

if __name__ == "__main__":
    provs = fetch_provinces()

    url = "https://kyfw.12306.cn/otn/queryAgencySellTicket/query"

    with open("11.final.txt", "w") as fd:
        for prov in provs:
            fetch_data(url, prov["chineseName"], fd)
            time.sleep(5)
