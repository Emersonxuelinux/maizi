# -*- coding:utf-8 -*-
# Importing base64 library because we'll need it ONLY in case 
#if the proxy we are going to use requires authentication
#-*- coding:utf-8-*-
import base64
from proxy import GetIp,counter
import logging

# 首先获取高速可用的代理ip
ips = GetIp().get_ips()


class ProxyMiddleware(object):
    # counter for http requests
    http_n = 0
    # counter for https requests
    https_n = 0

    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        # 对http链接处理
        if request.url.startswith("http://"):
            n = ProxyMiddleware.http_n
            n = n if n < len(ips['http']) else 0
            request.meta['proxy'] = "http://%s:%d" % (
                ips['http'][n][0], int(ips['http'][n][1])) # 取出http可用的代理ip和端口
            logging.info(
                'Squence - http: %s - %s' % (n, str(ips['http'][n])))
            ProxyMiddleware.http_n = n + 1
        # 对https链接处理
        if request.url.startswith("https://"):
            n = ProxyMiddleware.https_n
            n = n if n < len(ips['https']) else 0         
            request.meta['proxy'] = "https://%s:%d" % (
                ips['https'][n][0], int(ips['https'][n][1]))  # 取出https可用的代理ip和端口
            logging.info(
                'Squence - https: %s - %s' % (n, str(ips['https'][n])))
            ProxyMiddleware.https_n = n + 1
