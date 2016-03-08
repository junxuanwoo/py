# -*- coding: utf-8 -*-
#梧桐理财
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
from DBHelper1 import DBConn
from WTLC.items import WTLC_product
from bs4 import BeautifulSoup

class WTLC_Spider(Spider):
    #梧桐理财
    name = "WTLC"
    allowed_domains = ["www.91wutong.com"]
    conn = DBConn.get_instance()
    #随心投
    start_urls = conn.getUrls('http://www.91wutong.com/pts/product/products.htm?transfer=0&qidian=0&status=0&youhui=0&leftday=0&discount_money=0&page=',
                              0, '', '马上投资', 0)
    print start_urls

    def start_requests(self):
        #print self.start_urls
        for url in self.start_urls:
            yield scrapy.Request(url, callback = self.parse_url, encoding='utf-8')

    def parse_url(self, response):
        sel = Selector(response)
        #获取跳转链接
        urls = sel.xpath('//a[@class="btn btn-primary btn-small"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback = self.parse_sxt, encoding='utf-8')

    def parse_sxt(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = WTLC_product()

        item['platformid'] = 'P00608'# 平台ID
        item['producttype'] = '随心投'# 产品类型
        item['productname'] = sel.xpath('//div[@class="fl bold t2"]/text()').extract()[0] # 产品名称
        item['productid'] = re.search(r'\d+', item['productname']).group(0)# 产品ID
        info = sel.xpath('//div[@class="mb-sm-3 invest_total"]/text()').extract()[0]
        result = re.findall(r'\d+', info)
        item['amount'] = int(result[0])*10000
        item['balance'] = int(result[1])*10000
        item['maxrate'] = sel.xpath('//div[@class="wd-100 f50 text-primary number"]/text()').extract()[0]
        item['minrate'] = item['maxrate']
        item['startdate'] = sel.xpath('//div[@class="wd-33 fl text-left"]/text()').extract()[0]
        item['enddate'] = sel.xpath('//div[@class="wd-33 fl text-center"]/text()').extract()[0].strip()
        item['term'] = sel.xpath('//div[@class="wd-21 fl pl-4"]/div[@class="wd-100 f50 number"]/text()').extract()[0].strip()
        item['termunit'] = sel.xpath('//div[@class="wd-21 fl pl-4"]/div[@class="wd-100 f50 number"]/span/text()').extract()[0].strip()
        item['repaymentmethod'] = sel.xpath('//div[@class="wd-34 fl text-right"]/span/../text()').extract()[1].strip()

        values = (item['platformid'], item['producttype'], item['productname'].encode('utf-8'), item['productid'],
                  item['amount'], item['balance'], item['maxrate'].encode('utf-8'),
                  item['minrate'].encode('utf-8'), item['startdate'].encode('utf-8'), item['enddate'].encode('utf-8'),
                  item['term'], item['termunit'].encode('utf-8'), item['repaymentmethod'].encode('utf-8'), )
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
