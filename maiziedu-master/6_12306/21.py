# -*- coding: utf-8 -*-

import time
import json

import requests
import pymysql.cursors

def fetch_provinces():
    url = "https://kyfw.12306.cn/otn/userCommon/allProvince"

    try:
        s = requests.get(url, verify = False)
    except Exception, e:
        print "fetch provinces. " + url
        raise e

    j = json.loads(s.content)
    return j["data"]

def fetch_data(url, province, cursor):
    sql = "INSERT IGNORE INTO `agencys` (`province`, `city`, `county`,\
            `address`, `name`, `windows`, `start`, `end`) VALUES\
            (%s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        s = requests.get(url, params = {"province":province, "city":"", "county":""}, verify = False)
    except Exception, e:
        print "requests url fail.", url, province.encode("utf-8")
        return

    datas = json.loads(s.content)

    for data in datas["data"]["datas"]:
        cursor.execute(sql, (data["province"], data["city"],
                            data["county"], data["address"],
                            data["agency_name"], data["windows_quantity"],
                            data["start_time_am"] + u"00",
                            data["stop_time_pm"] + u"00"))

if __name__ == "__main__":
    provs = fetch_provinces()

    url = "https://kyfw.12306.cn/otn/queryAgencySellTicket/query"

    conn = pymysql.connect(host = 'localhost', port = 3306,
                                user = '12306',
                                password = '12306',
                                db = '12306-train',
                                charset = 'utf8')
    with conn.cursor() as cursor: 
        for prov in provs:
            fetch_data(url, prov["chineseName"], cursor)
            conn.commit()
            time.sleep(5)


