# -*- coding: utf-8 -*-

import os
import re
import sys
import urllib2
from crawler.rulesConfig import urlList

#多进程,一个爬取,一个解析
class CrawlProgress():
    urls = []

    def start(self):
        os.chdir(sys.path[0])

        listLenth = len(urlList)
        for num in xrange(listLenth):
            domain = urlList[num][0]
            key = urlList[num][2]
            for url in self.urls:
                os.system("scrapy crawl all -a allowed_domains={} -a start_urls={} -a rule_key={}".format(
                domain, url, key))

    def parseUrl(self):
        for ul in urlList:
            minId = ul[1]
            count = ul[4]
            regex = re.compile(ul[3])
            while (1):
                url = "{}{}{}".format(ul[0], str(minId), ul[2])
                html = urllib2.urlopen(url).read()
                if len(regex.findall(html)) > count:
                    #匹配到满足条件的flagWord标记
                    self.urls.append(url)
                    minId += 1
                else:
                    break
if __name__ == "__main__":
    pro = CrawlProgress()

    # 获取每个产品的全链接
    pro.parseUrl()

    # 运行爬虫
    pro.start()