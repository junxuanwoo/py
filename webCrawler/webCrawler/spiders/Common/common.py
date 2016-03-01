# -*- coding: utf-8 -*-
import urllib2
import re

#获取每一个在售新标产品的最大页数(即有多少页的新标产品还在售)
#@leftUrl: url中可变的id的左半部分url
#@minId: url可变部分min id
#@rightUrl: url中可变的id的右半部分url
#@flagWord: 判定标记字符串
def common_getUrls(leftUrl, minId, rightUrl, flagWord):
    #循环判断url集合新标产品最大页数
    start_urls = []
    regex = re.compile(flagWord)
    while (1):
        url = leftUrl + str(minId) + rightUrl
        html = urllib2.urlopen(url).read()
        if (regex.search(html)):
            #获取产品跳转链接
            start_urls.append(url)
            minId += 1
        else:
            break
    return start_urls