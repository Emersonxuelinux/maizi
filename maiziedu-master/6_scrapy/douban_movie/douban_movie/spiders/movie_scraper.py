# -*- coding: utf-8 -*-
import scrapy
import pdb
from douban_movie.items import DoubanMovieItem
import re

headers = {
        'Accept':'*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        # 暂时不用cookie试试。 'Cookie':'bid=yAMd84V94sg; ps=y; ll="118318"; ue="hughohoho@gmail.com"; dbcl2="113667643:Aku7Uxb2dSY"; ck=Hwp_; ap=1; __utma=30149280.743563175.1422940286.1466065258.1466501870.13; __utmc=30149280; __utmz=30149280.1465956799.11.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmv=30149280.11366; __utma=223695111.1387345932.1466501870.1466501870.1466501870.1; __utmc=223695111; __utmz=223695111.1466501870.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); push_noty_num=0; push_doumail_num=4; _pk_id.100001.4cf6=f63938885dc79088.1466501870.2.1466574649.1466503191.; _pk_ses.100001.4cf6=*'
        'Host':'movie.douban.com',
        'Referer':'https://movie.douban.com/explore',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
        }

cookies = {}
class movie_scraper(scrapy.Spider):
    name = 'douban_movie_spider'
    # 设置headers，注意每行要加逗号
    allowed_domains = ["douban.com"]

    def start_requests(self):
        global headers

        url = "https://movie.douban.com/explore"
        # yield scrapy.Request(url = url, headers = headers)
        return [
            scrapy.Request(url=url, headers=headers, ),
        ]
    
    def parse(self,response):
        global headers
        global cookies
        # url = 'https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0'
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0'
        # 获取服务器响应的cookie值并提取为列表
        cookie_values = [x.split('=')[1] for x in response.headers['Set-Cookie'].split(';')]
        cookies = {
            'bid': cookie_values[0],
            'Expires': cookie_values[1],
            'Domain': cookie_values[2],
            'Path': cookie_values[3],
        }

        yield scrapy.Request(
                url=url,
                callback=self.parse_movie,
                cookies=cookies,
                headers=headers,
            )

    def parse_movie(self, response):
        global cookies
        global headers
        # 从返回的正文中取出[{...}]之间的内容
        dict_str = re.search('\[\{.*}]', response.body).group()
        # 取出所有{。。。}之间的内容，是dict格式的字符串
        temp = re.findall('\{.*?}', dict_str)
        # 替换布尔量，否则报错
        temp1 = [x.replace('false','False') for x in temp]
        temp2 = [x.replace('true','True') for x in temp1]
        # 替换转义符号
        temp3 = [x.replace('\\', '') for x in temp2]
        # 使用eval把正确的字符串转为对应的类型
        dict_list = [eval(x) for x in temp3]
        for x in dict_list:
            item = DoubanMovieItem()
            item['title'] = x['title']
            item['post_urls'] = [x['cover'], ]
            # pdb.set_trace()
            yield scrapy.Request(
                    url=x['url'],
                    meta={'item': item},  # 通过meta把item传送到另外一个页面抓取中
                    cookies=cookies,
                    headers=headers,
                    callback=self.parse_intro,
                    # dont_filter=True,
                )

    def parse_intro(self, response):
        item = response.meta['item']
        item['intro'] = response.xpath('//*[@id="link-report"]/span/text()').extract()[0]

        yield item
