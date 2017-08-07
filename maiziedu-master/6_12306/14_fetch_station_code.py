# -*- coding: utf-8 -*-

import time
import datetime
import json

import requests

def fetch_stations(fd):
    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8936"

    try:
        s = requests.get(url, verify = False)
    except Exception, e:
        print "fetch stations fail. " + url
        raise e

    station_str = s.content.decode("utf-8")
    
    stations = station_str.split(u"@")

    for i in range(1, len(stations)):
        station = stations[i].split(u"|")
        out = station[1] + u" " + station[2] + u"\n"
        fd.write(out.encode("utf-8"))
        #fd.write("\n")
        #print s

if __name__ == "__main__":

    with open("14.txt", "w") as fd:
        fetch_stations(fd)