#coding=utf-8

import sys,os
import urllib2
import re
from scrapy.selector import Selector
from bs4 import BeautifulSoup


def getXpath():
    url = 'https://dai.kesucorp.com/project/list'
    response = urllib2.urlopen(url)
    html= response.read()
    sel = Selector(response)
    product_urls  = sel.xpath('//div')[0].extract()
    print product_urls
    
def getMaxId(leftUrl, minId, rightUrl, flagWord):
    #循环判断url集合新标产品最大页数
    start_urls = []
    regex = re.compile(flagWord)
    while (1):
        url = leftUrl + str(minId) + rightUrl
        print url
        html = urllib2.urlopen(url).read()
        print url
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


def parse_url():
    start_urls = []
    urls = common_getUrls('http://www.mindai.com/grtzlc?app_type=youxuan&ui_type=inline&order=default&currentPage=', 1, '', 'qq')
    print "urls = ", urls
    for url in urls:
        response = urllib2.urlopen(url)
        sel = Selector(response)
        #nodes保存的是立即抢购的节点a
        nodes = sel.xpath('//td[@class="td_first sign"]/a[@class="td_but red"]')
        for node in nodes:
            soup = BeautifulSoup(node)
            product_url = soup.a['href']
            print "product_url = ", product_url
            start_urls.append(product_url)

#http://www.dezhong365.com/invest?state=0
#start_urls = getMaxId("http://www.dezhong365.com/invest?state=", 0, "", "立即投标")
#start_urls = getMaxId("http://www.mindai.com/grtzlc?app_type=youxuan\ui_type=inline&order=default&currentPage=", 1, "", "立即抢购")
#print start_urls
getXpath()
