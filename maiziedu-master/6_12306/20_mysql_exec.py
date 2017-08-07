# -*- coding: utf-8 -*-

import pymysql.cursors

if __name__ == "__main__":
    # 连接数据库，用户名和密码都是sql中创建的
    conn = pymysql.connect(
        host = 'localhost', port = 3306,
        user = '12306',
        password = '12306',
        db = '12306-train',
        charset = 'utf8')

    try:
        # 这种with写法有点像文件读写的with写法，这里执行插入操作
        with conn.cursor() as cursor:
            sql = "INSERT IGNORE INTO `example` VALUES (%s, %s, %s)"
            cursor.execute(sql, (u"G1001", u"武汉", u"深圳"))
            cursor.execute(sql, (u"G1002", u"武汉", u"深圳"))
            cursor.execute(sql, (u"G1003", u"武汉", u"深圳"))
        # 插入后需要提交
        conn.commit()
        # 这里执行查询操作
        with conn.cursor() as cursor:
            sql = "SELECT `code`, `start`, `end` FROM `example`"
            cursor.execute(sql)
            results = cursor.fetchall()
            for result in results:
                print result[0], result[1], result[2]

    finally:
        conn.close()














# vim: set ts=4 sw=4 sts=4 tw=100 et:
