# -*- coding: utf-8 -*-
#安心金融
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spider import Spider
from DBHelper1 import DBConn
from AXJR.items import AXJR_product
from bs4 import BeautifulSoup

class AXJR_Spider(Spider):
    #安心金融
    name = "AXJR"
    allowed_domains = ["www.anxinjr.com"]
    conn = DBConn.get_instance()
    start_urls = ['', '', '']
    start_urls = conn.getUrls('http://www.anxinjr.com/listall?page=', 1, '', '立即投资')
    print "start_urls = ", start_urls

    def parse(self, response):
        sel = Selector(response)
        #获取当前列表页中所有在售新标的url跳转链接(a节点)
        product_urls  = sel.xpath('//div[@class="op"]/a').extract()
        for product_url in product_urls:
            #print product_url
            soup = BeautifulSoup(product_url, 'lxml')
            #print soup.a(text=True)[0].encode("utf-8")
            if soup.a(text=True)[0].encode("utf-8") == "立即投资":
                print soup.a['href']
                newUrl = 'http://www.anxinjr.com' + soup.a['href']
                #print "newUrl = ", newUrl
                yield scrapy.Request(newUrl, callback = self.parse_id_fy, encoding = 'utf-8')

    def parse_id_fy(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = AXJR_product()

        item['productName'] = sel.xpath('//div[@class="infoList2 clearfx"]/div/h2/text()')[0].extract()#产品名称
        #总额,期限,收益都在一个大的模块里不同的p节点
        tmp = sel.xpath('//ul[@class="m1 clearfx"]/li/ul/li/p/text()').extract()
        item['amount'] = tmp[4].replace('万','')#标的总额(万元)
        item['term'] = tmp[2]#期限(月)
        item['annualRate'] = tmp[0]#年利率(%)
        item['balance'] = sel.xpath('//div[@class="p cur_balance"]/p/text()')[1].extract().replace(r'￥', '')#可投金额(元)

        item['amountunit'] = '万元'
        item['amountunit'] = '万元'
        item['termunit'] = '月'
        item['balanceunit'] = '元'

        values = (item['productName'].encode("utf-8"),item['amount'],item['amountunit'].encode("utf-8"),
                   item['annualRate'],item['term'], item['termunit'].encode("utf-8"),item['balance'].replace('元',''),item['balanceunit'].encode("utf-8"))
        items.append(item)
        sql = 'insert into anxinjinrong_product_info(productname,amount,amountunit,annualrate,term,termunit,balance,balanceunit) values( %s,%s,%s,%s,%s,%s,%s,%s)'
        par = values
        prductName = "".join(item['productName'])
        a = self.conn.find_product(prductName,'anxinjinrong_product_info')
        if a == 0:
             self.conn.query(sql, par)
        else:
             print '此数据数据库中已存在！'
        return items

