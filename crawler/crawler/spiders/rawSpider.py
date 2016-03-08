# -*- coding: utf-8 -*-

#爬虫Spider模块

import re
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
from crawler.items import ProductItem
from crawler.rulesConfig import productRule
from crawler.spiders.db import DBConn

class RawSpider(Spider):

    name = "all"
    conn = DBConn.get_instance()

    def __init__(self, allowed_domains, start_urls, rule_key):
        self.allowed_domains = allowed_domains
        self.start_urls = [start_urls]
        self.rule_key = rule_key

    def start_requests(self):
        print 'start_request++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, callback=self.prase_product, encoding='utf-8')

    def prase_product(self, response):
        print 'prase_product++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        product = productRule[self.rule_key]

        sel = Selector(response)
        item, items = ProductItem(), []

        #还款期限
        test = sel.xpath(product['term']['xpath']).extract()[product['term']['ruleIndex']]
        if product['term']['regex']:
            item['term'] = re.search('', test)
        else :
            item['term'] = test
        if item['term'] is not None:
            print '还款期限——————————————————————————————————————',item['term']

        values = (item['platformid'],item['producttype'],item['productname'].encode('utf-8'),item['productid'],item['amount'].encode('utf-8'),
                  item['balance'].encode('utf-8'),item['maxrate'].encode('utf-8'),item['minrate'].encode('utf-8'),
                  item['startdate'].encode('utf-8'),item['enddate'],item['term'],item['termunit'].encode('utf-8'),item['repaymentmethod'].encode('utf-8'))
        items.append(item)
        sql = 'insert into newbid_product_info_test1(platformid,producttype,productname,productid,amount,balance,maxrate,minrate,' \
              'startdate,enddate,term,termunit,repaymentmethod) values( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        par = values
        a = self.conn.find_product(item['platformid'], item['productid'])
        if a == 0:
            self.conn.query(sql, par)
        else:
            print '此数据数据库中已存在！'
        return items

