# -*- coding:utf-8 -*-
import urllib
import datetime
import pdb

def download_stock_data(stock_list):  # 下载全部记录
    # 对列表中的股票id一一获取记录
    for sid in stock_list:
        url = 'http://table.finance.yahoo.com/table.csv?s=' + sid
        fname = sid + '.csv'
        print 'downloading %s from %s' % (fname,url)
        urllib.urlretrieve(url,fname)

def download_stock_data_in_period(stock_list,start,end): # 下载指定时间段记录
    for sid in stock_list:
        params = {'a': start.month -1,'b': start.day,'c': start.year,
               'd': end.month - 1,'e': end.day, 'f': end.year, 's':sid}
        url = 'http://table.finance.yahoo.com/table.csv?s='
        qs = urllib.urlencode(params)
        url = url + qs
        fname = '%s_%d%d%d_%d%d%d.csv' % (sid,start.year,start.month,start.day,
                                         end.year,end.month,end.day)
        print 'downloading %s from %s' % (fname,url)
        if urllib.urlopen(url).getcode() == 200:
            urllib.urlretrieve(url,fname)
        else: print '没有获取'



if __name__ == '__main__':
    stock_list = ['300001.sz','300002.sz']
    end = datetime.date(year=2015,month=5,day=17)
    start = datetime.date(year=2015,month=4,day=17)
    download_stock_data_in_period(stock_list,start,end)
