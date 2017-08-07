# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime

import pymysql.cursors
# 需要指明类加载路径
# 因为本来是scrapy做的，我们要自己启动就需要自己动手
project_path = os.path.dirname(os.path.abspath(__file__ + "/.."))
sys.path.insert(0, project_path)


# import the spiders you want to run
from spiders.agencys import AgencysSpider
from spiders.stations import StationsSpider
from spiders.trains import ScheduleSpider
from spiders.tickets import TicketsSpider

# scrapy api imports
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

'''
import logging
from scrapy.utils.log import configure_logging

#configure logging
configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s'
)
'''

settings = get_project_settings()

crawler = CrawlerProcess(settings)

@defer.inlineCallbacks
def crawl():
    # 把本轮轮次数据的插入放在这里
    n = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    turn = int(time.time() / 86400)

    conn = pymysql.connect(host = 'localhost', port = 3306, 
                                    user = '12306',
                                    password = '12306',
                                    db = '12306-train',
                                    charset = 'utf8')
    with conn.cursor() as cursor:
        cursor.execute("INSERT IGNORE INTO `turns` VALUES (%s, %s)", (turn, n))
    conn.commit()
    conn.close()
    # 然后依次执行爬虫
    yield crawler.crawl(AgencysSpider, turn)
    yield crawler.crawl(StationsSpider, turn)
    yield crawler.crawl(ScheduleSpider, turn)
    yield crawler.crawl(TicketsSpider, turn)

    print "crawler over"

crawl()
crawler.start()















# vim: set ts=4 sw=4 sts=4 tw=100 et:
