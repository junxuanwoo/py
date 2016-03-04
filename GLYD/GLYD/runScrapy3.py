#!/usr/bin/env python
#coding=utf-8

#程序功能：循环间隔执行爬虫


import time
from scrapy import cmdline

while(1):
    cmdline.execute("scrapy crawl GLYD".split())
    time.sleep(10)
