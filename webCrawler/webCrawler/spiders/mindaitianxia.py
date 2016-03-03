# -*- coding: utf-8 -*-
#民贷天下

from scrapy.spiders import Spider
from scrapy.selector import Selector
from webCrawler.items import MDTX_product
from Common.common import common_getUrls
#from DBHelper.DBcon import MySQL
from bs4 import BeautifulSoup
import MySQLdb
import urllib2

class CTCF_Spider(Spider):
    #民贷天下
    name = "MDTX"
    start_urls = []
    allowed_domains = ["http://www.mindai.com/"]
    #http://www.mindai.com/grtzlc?app_type=youxuan&ui_type=inline&order=default&currentPage=1
    urls = common_getUrls('http://www.mindai.com/grtzlc?app_type=youxuan&ui_type=inline&order=default&currentPage=', 1, '', '立即抢购')
    print "urls = ", urls
    for url in urls:
        pass
        response = urllib2.urlopen(url)
        sel = Selector(response)
        #nodes保存的是立即抢购的节点a
        nodes = sel.xpath('//td[@class="td_first sign"]/a[@class="td_but red"]')
        for node in nodes:
            soup = BeautifulSoup(node)
            product_url = soup.a['href']
            print "product_url = ", product_url
            start_urls.append(product_url)

    def start_requests(self):
        pass

    def parse(self, response):
        sel = Selector(response)
        items = []
        values = []
        item = MDTX_product()

        product =sel.xpath('//div[@class="up"]')
        #余额
        item['balance'] = product[0].xpath('div/i[@class="cs"]/text()')[0].extract().encode("utf-8")
        #总金额
        item['amount'] = product[0].xpath('div[@class="jian"]/text()')[0].extract().encode("utf-8")
        #产品名称
        item['productName'] = product[0].xpath('div[@class="up"]/a/text()')[0].extract().encode("utf-8")
        #年利率
        item['annualRate'] = product[1].xpath('//span[@class="nhy"]/i/text()')[0].extract().encode("utf-8")
        #第二个年利率,去除'+'
        item['annualRate'] = product[1].xpath('//span[@class="nhy"]/i/font/text()')[0].extract().encode("utf-8")
        #期限
        item['term'] = product[2].xpath('//span[@class="zq"]')[0].extract().encode("utf-8")

        values.append(item['productName'],[item['amount'], item['balance'], item['term'], item['annualRate']])
        items.append(item)
        try:
            conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
            cur=conn.cursor()
            conn.select_db('product_info')
            cur.executemany('insert into renrendai(amount, annualRate, term, safeguard,prepaymentRate, repaymentMethod, progress,remainingTime,balance, proid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            print '数据库操作异常！'

        return items