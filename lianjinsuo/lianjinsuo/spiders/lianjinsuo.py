#coding=utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from lianjinsuo.items import YYS_product
import urllib2
import re
from bs4 import BeautifulSoup
import MySQLdb

#获取每一个在售新标产品的最大页数(即有多少页的新标产品还在售)
#@leftUrl: url中可变的id的左半部分url
#@minId: url可变部分min id
#@rightUrl: url中可变的id的右半部分url
#@flagWord: 判定标记字符串
def getUrls(leftUrl, minId, rightUrl, flagWord):
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
            #获取产品跳转链接
            start_urls.append(url)
            minId += 1
        else:
            break
    return start_urls

class LJSSpider(Spider):

    #联金所
    name = "LJS"
    allowed_domains = ["www.uf-club.com"]
    #月月升http://www.uf-club.com/frontyysPkgDetail.do?pkgId=870
    #frontyysPkgDetail.do?pkgId=870
    yys_urls = getUrls("https://www.uf-club.com/yysPkgListInit.do?curPage=", 1, "", "加入")
    #联金添财
    ljtc_urls = getUrls("http://www.uf-club.com/borrowIndex.do?curPage=", 1, "", "加入")
    #合并2个存放产品链接的list
    start_urls = yys_urls + ljtc_urls

    def parse(self, response):
        sel = Selector(response)
        items = []
        values = []
        item = YYS_product()
        product =sel.xpath('//div[@class="fn-clear  mb25"]/dl')

        item['yys']['amount']
        item['amount'] = product[0].xpath('dd/em/text()')[0].extract().encode("utf-8")
        item['annualRate'] = product[1].xpath('dd/em/text()')[0].extract().encode("utf-8")
        item['term'] = product[2].xpath('dd/em/text()')[0].extract().encode("utf-8")
        item['safeguard']=sel.xpath('//span[@class="fn-left basic-value last"]/text()')[0].extract().encode("utf-8")
        item['prepaymentRate']=sel.xpath('//span[@class="fn-left basic-value num"]/em/text()')[0].extract().encode("utf-8")
        item['repaymentMethod']=sel.xpath('//span[@class="fn-left basic-value"]/text()')[0].extract().encode("utf-8")
        item['proid'] = response.url.split("loanId=")[1]
        values.append([item['amount'], item['annualRate'], item['term'], item['safeguard'], item['prepaymentRate'], item['repaymentMethod'], '', '', '', item['proid']])
        items.append(item)

        # try:
        #     conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
        #     cur=conn.cursor()
        #     conn.select_db('product_info')
        #     cur.executemany('insert into renrendai(amount, annualRate, term, safeguard,prepaymentRate, repaymentMethod, progress,remainingTime,balance, proid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', values)
        #     conn.commit()
        #     cur.close()
        #     conn.close()
        # except MySQLdb.Error:
            # print '数据库操作异常！'

        return items



print soup.title.string

print soup.p

print soup.a

print soup.find_all('a')

print soup.find(id='link3')

print soup.get_text()