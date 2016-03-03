# -*- coding: utf-8 -*-
#汇付四海

from scrapy.spiders import Spider
from scrapy.selector import Selector
from webCrawler.items import HFSH_product
from Common.common import common_getUrls
from DBHelper.DBcon import MySQL
#from bs4 import BeautifulSoup

class CTCF_Spider(Spider):
    #汇付四海
    name = "HFSH"
    allowed_domains = ["http://www.huifusihai.com/invest.do"]
    db = MySQL()
    start_urls = common_getUrls('http://www.huifusihai.com/invest.do?page=', 1, '', '招标中')

    def parse(self, response):
        sel = Selector(response)
        items = []
        values = []
        item = HFSH_product()
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

        return items
