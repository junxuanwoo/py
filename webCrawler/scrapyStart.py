# -*- coding: utf-8 -*-

import os
import sys
from webCrawler.rulesConfig import projectName

def start():
    print sys.path[0]
    os.chdir(sys.path[0])
    number = len(projectName)
    for n in xrange(number):
        os.system("scrapy crawl YBJR")#.format(projectName[n]))

if __name__ == "__main__":
    # 运行爬虫
    start()