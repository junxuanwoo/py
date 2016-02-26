#coding=utf-8

import sys,os
import urllib2
import re

def getMaxId(leftUrl, minId, rightUrl, flagWord):
    #循环判断url集合新标产品最大页数
    start_urls = []
    regex = re.compile(flagWord)
    while (1):
        url = leftUrl + str(minId) + rightUrl
        html = urllib2.urlopen(url).read()
        #转换编码
        #html = unicode(html, "gb2312").encode("utf8")
        #print html
        if (regex.search(html)):
            #匹配到flagWord标记
            start_urls.append(url)
            minId += 1
        else:
            break
    return start_urls
#http://www.dezhong365.com/invest?state=0
start_urls = getMaxId("http://www.dezhong365.com/invest?state=", 0, "", "立即投标")
print start_urls
