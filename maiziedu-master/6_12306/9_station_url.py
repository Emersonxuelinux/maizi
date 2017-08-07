# -*- coding: utf-8 -*-

import time

import requests
from bs4 import BeautifulSoup

def fetch_data(url, bureau, desc, fd):
    try:
        s = requests.get(url)
    except Exception, e:
        print "requests url fail. " + url
        return

    b = BeautifulSoup(s.content, "lxml")
    datas = b.select("tbody > tr")
    # 前两行不是数据
    if len(datas) <= 2:
        # 注意中文要encode一下
        s = "find nothing " + url + " " + bureau.encode("utf-8") + " " + desc.encode("utf-8")
        print s
        fd.write(s + "\n")

    for i in range(0, len(datas)):
        if i < 2:
            continue
        infos = datas[i].find_all("td")
        # 同样中文写入要交u''
        out = u""
        for info in infos:
            out += info.text
            out += u"， "

        out += bureau + u"， " + desc
        s = out.encode("utf-8")
        fd.write(s)
        fd.write("\n")
        print s


if __name__ == "__main__":

    url = "http://www.12306.cn/mormhweb/kyyyz/"

    try:
        s = requests.get(url)
    except Exception, e:
        print "requests url fail. " + url
        raise e

    b = BeautifulSoup(s.content, "lxml")
    names = b.select("#secTable > tbody > tr > td")

    sub_urls = b.select("#mainTable td.submenu_bg > a")
    with open("9.2.txt", "w") as fd:
        for i in range(0, len(names)):
            sub_url1 = url + sub_urls[i * 2]["href"][2:]
            print sub_url1
            # 中文需要加u''
            fetch_data(sub_url1, names[i].text, u"车站", fd)
            # 避免太快被12306屏蔽ip
            time.sleep(5)

            sub_url2 = url + sub_urls[i * 2 + 1]["href"][2:] 
            print sub_url2
            fetch_data(sub_url2, names[i].text, u"乘降所", fd)
            time.sleep(5)


    



    


    














# vim: set ts=4 sw=4 sts=4 tw=100 et:
