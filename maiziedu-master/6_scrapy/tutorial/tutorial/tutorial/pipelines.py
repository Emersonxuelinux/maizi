# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
# 这里把数据库的相关参数设置好
DBKWARGS={'db':'test','user':'root', 'passwd':'123456',
    'host':'localhost','use_unicode':True, 'charset':'utf8'}

class TutorialPipeline(object):

    def __init__(self):
        try:
            # 传入设置好的参数与mysql建立连接
            self.con = MySQLdb.connect(**DBKWARGS)
        except Exception,e:
            print "Connect db error:",e


    def process_item(self, item, spider):
        # 通过连接建立游标，准备执行sql语句
        cur = self.con.cursor()
        # sql语句中有三个占位符，对应后面替换的数据
        sql = "insert into dmoz_book values(%s,%s,%s)"
        lis = (''.join(item["title"]),''.join(item["link"]),
            ''.join(item["desc"]))
        try:
            cur.execute(sql,lis)
        except Exception,e:
            print "Insert error:",e
            self.con.rollback()
        else:
            self.con.commit()
        cur.close()
        return item

    def __del__(self):
        try:
            self.con.close()
        except Exception,e:
            print "Close db error",e