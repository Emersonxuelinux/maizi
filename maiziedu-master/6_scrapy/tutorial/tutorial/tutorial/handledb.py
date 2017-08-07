# -*- coding:utf-8 -*- 

'''
Function:handle database's any operation
Author:Wan Shitao
Email:wst.521@163.com
Date:2014.8.20
Reference:funcs.py
'''
'''
Twisted 是一个异步网络框架，不幸的是大部分数据库api实现只有阻塞式接口.
twisted.enterprise.adbapi为此产生，它是DB-API 2.0 API的非阻塞接口，可以访问各种关系数据库。
'''
from twisted.enterprise import adbapi
import MySQLdb


# 连接mysql


def get_db(**kwargs):
    '''connect database,return link resource'''
    try:
        db = MySQLdb.connect(**kwargs)
    except Exception, e:
        print "Link DB error:", e
    else:
        return db

# 创建表格,proxy中并没有用到这个方法
def create_table (data, primary, table, **kwargs):
    ''' Create table for storing resume data. '''
    # 这是建表sql语句，用了占位符
    sql='create table if not exists `%s`(%s) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci'
    # 这是python的列表解析式
    # 左边一个方括号是一个列表
    # 右边是可选参数，有传入主键就加上
    # data中是传入的建表需要的字段
    ps = ["`%s` text" % x for x in data] + ([primary, ] if primary else [])
    # 把列表中的字段名称拼接成字符串
    paras = ','.join(ps)
    # 再填充sql语句的占位符
    SQL = sql % (table, paras)
    # 调用另一个函数执行sql语句
    exec_sql(SQL, **kwargs)

# 执行sql语句的函数


def exec_sql(sql, data='', **kwargs):
    '''execute insert sql and other operation'''
    conn = get_db(**kwargs)
    cur = conn.cursor()
    if data == '':
        # 调用游标的sql语句执行函数
        cur.execute(sql)
    else:
        cur.execute(sql, data)
    # 执行之后调用函数获取全部结果，是一个列表
    result = cur.fetchall()
    # 提交这个结果
    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()
    return result

# 插入数据的方法


def insert_data(data_, table, **kwargs):
    '''insert data into database''' 
    insertSQL = "insert into `" + table + "`(%s) values (%s)"
    # 传入的data_是字典类型，这里获取所有键名
    # 其实就对应了表的字段名
    keys = data_.keys()
    # 把这些字段名拼接起来
    # 这个给insertSQL第一个占位符
    fields = ','.join(['`%s`' % k for k in keys])
    # 拼接多个占位符
    # 这个替换insertSQL第二个占位符
    qm = ','.join(['%s'] * len(keys))
    # 替换为新的sql语句
    # 这里的sql才是真正的sql语句，带确定数量的占位符
    sql = insertSQL % (fields, qm)
    # 从data_取出要插入的数据
    data = [data_[k] for k in keys]
    exec_sql(sql, data, **kwargs)


# adbapi连接数据库的方法
def adb_connect_db(db_type, **kwargs):
    '''
    db_type-->"MySQLdb"
    '''
    dbpool = adbapi.ConnectionPool(db_type, **kwargs)
    return dbpool

# adbapi插入数据库的方法


def adb_insert_data(item, table, db_type, **kwargs):
    keys = item.keys()
    fields = u','.join(keys)
    # 这里u''表示unicode码，为中文准备
    # 拼接出插入数据个数相同的占位符字符串
    qm = u','.join([u'%s'] * len(keys))
    insert_sql = "insert into `"+table+"`(%s) values (%s)"
    # 第一次替换占位符，得到最终带占位符的sql语句
    sql = insert_sql % (fields, qm)
    data = [item[k] for k in keys]
    # 调用adbapi连接数据库，这里db_type指明是mysql类型的数据库
    # 两个参数都定义在settings中了
    dbpool = adb_connect_db(db_type, **kwargs)
    # 执行sql语句
    # adbapi不需要获得游标
    d = dbpool.runOperation(sql, data)
    # 成功的话调用这个函数
    d.addCallback(insSuccess)
    # 失败的话调用这个函数
    d.addErrback(insFailed, item)
    # 关闭数据库连接
    dbpool.close()
    
def insSuccess(data):
    print "data inserted",data
    
def insFailed(exp,data):
    print "insert failed",data,"error:",exp.getErrorMessage()
