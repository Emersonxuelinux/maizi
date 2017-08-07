# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb

class CollectipsPipeline(object):

    def process_item(self, item, spider):
        # 从settings获取数据库相关参数DBKWARGS
        DBKWARGS = spider.settings.get('DBKWARGS')
        # 使用获取的数据库参数建立连接
        con = MySQLdb.connect(**DBKWARGS)
        # 获取数据库游标
        cur = con.cursor()
        # 插入数据表的sql语句
        sql = ("insert into proxy(IP,PORT,TYPE,POSITION,SPEED,LAST_CHECK_TIME) "
            "values(%s,%s,%s,%s,%s,%s)")
        # 占位符对应的数据
        lis = (item['IP'],item['PORT'],item['TYPE'],item['POSITION'],item['SPEED'],
            item['LAST_CHECK_TIME'])
        try:
            cur.execute(sql,lis)
        except Exception,e:
            print "Insert error:",e
            con.rollback()
        else:
            con.commit()
        cur.close()
        con.close()
        return item
