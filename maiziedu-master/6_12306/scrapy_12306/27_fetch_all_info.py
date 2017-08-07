# -*- coding: utf-8 -*-
import pymysql.cursors

if __name__ == '__main__':

    conn = None
    conn = pymysql.connect(host = 'localhost',
                                port = 3306,
                                user = '12306',
                                passwd = '12306',
                                db = '12306-train',
                                charset = 'utf8')

    print("open mysql succ")
    # 把每个车次站点信息都取出来
    # 包括一个车次上一个起点站到所有能到站点的记录
    select = "select * from train_infos"
#    insert = "update books set `ip`={0}, `pv`={1} where `url` = '{2}'"
    # 存放处理过的车次站点信息
    schedules = {}
    with conn.cursor() as cursor:
        cursor.execute(select)
        count = 0
        # 这里的results指每一行的记录，有三个字段：车次，站名，站序
        for results in cursor.fetchall():
            if results[0] not in schedules:
                # results[1]-站点序号
                # results[2]-站名
                schedules[results[0]] = {results[1]: results[2]}
            else:
                # 如果已经采集过了就更新一下
                # 二维字典：[车次][站序]：站名
                # 这样做是基于没有两个车次有相同序号的相同站名
                schedules[results[0]][results[1]] = results[2]
    # 打印有多少个车次
    print len(schedules)
    # 存放任意两站之间的路线
    routes = {}
    sum = 0
    # 遍历车次，也就是字典的键
    for key in schedules:
        # 取出这个车次的所有路线记录
        route = schedules[key]
        # 先对这个车次经过的路线排序
        seq = sorted(route)
        len1 = len(seq)
        # 一个车次路线上任意两个站点之间都能通行
        # 这是排列组合的方式
        sum += len1 * (len1 - 1) / 2
        for i in range(0, len1):
            if route[seq[i]] not in routes:
                tmp = set()
                # 字典的key是站名
                # value是一个集合，存储了所有可以从key出发到达的站
                routes[route[seq[i]]] = tmp
            else:
                tmp = routes[route[seq[i]]]
            for j in range(i + 1, len1):
                tmp.add(route[seq[j]])

    print sum
    sum = 0
    for route in routes:
        print route.encode("utf-8")
        for s in routes[route]:
            print s.encode("utf-8"),
        print ""
        sum += len(route)
        
    print sum
