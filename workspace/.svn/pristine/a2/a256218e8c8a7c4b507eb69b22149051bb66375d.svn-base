# -*- coding: utf-8 -*-
#和信贷
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spider import Spider
from DBHelper1 import DBConn
from HXD.items import HXD_product
from bs4 import BeautifulSoup

class HXD_Spider(Spider):
    #和信贷
    name = "HXD"
    allowed_domains = ["member.hexindai.com"]
    conn = DBConn.get_instance()
    urls_cj = conn.getUrls('https://member.hexindai.com/invest-state_-period_-bidtype_-sortkey_-sortvalue_-pageid_'
                           '', 1, '.html', '去出借')
    urls_hb = conn.getUrls('https://member.hexindai.com/pocket-pageid_', 1, '.html', '加入')
    start_urls = []

    def start_requests(self):
        for url_cj in self.urls_cj:
            yield scrapy.Request(self.urls_cj, callback = self.parse_cj_urls, encoding = 'utf-8')
        #for url_hb in self.urls_hb:
         #   yield scrapy.Request(self.urls_hb, callback = self.parse_hb_urls, encoding = 'utf-8')

    #出借项目解析函数
    def parse_cj_urls(self, response):
        sel = Selector(response)
        #获取当前列表页中所有在售新标的url跳转链接(a节点)
        #product_urls  = sel.xpath('//a[@class="btn_red_little btn_little"]').extract()
        product_urls  = sel.xpath('//tr/td/em[@class="ico_credit_new"]../../td[@class="td_right"]/a[@class="btn_red_little btn_little"]').extract()
        #product_urls  = sel.xpath('//tr[@class="m20r_2w"]/td/font/b/text()').extract()#20个tr
        for product_url in product_urls:
            print product_url
            soup = BeautifulSoup(product_url, 'lxml')
            newUrls = 'https://member.hexindai.com' + soup.a['href']
            yield scrapy.Request(newUrls, callback = self.parse_cj, encoding = 'utf-8')

    def parse_cj(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = HXD_product()

        item['productName'] = sel.xpath('//div[@class="biao_con_l_tit"]/h2/text()')[0].extract()#产品名称
        #tmp取出是￥100000.00
        item['amount'] = sel.xpath('//div[@class="biao_con_l_con"]/div[@class="account"]/span/text()')[0].extract().replace('￥', '')#标的总额(元)
        item['balance'] = sel.xpath('//div[@class="biao_con_r_con"]/p/text()')[0].extract().replace(r'可投金额：', '')#可投金额(元)
        item['term'] = sel.xpath('//span[@class="time_limit_font"]/text()')[0].extract()#期限(月)
        item['annualRate'] = sel.xpath('//span[@class="apr_font"]/text()')[0].extract()#年利率(%)
        item['amountunit'] = '元'
        item['termunit'] = '月'
        item['balanceunit'] = '元'

        values = (item['productName'].encode("utf-8"),item['amount'],item['amountunit'].encode("utf-8"),
                   item['annualRate'],item['term'], item['termunit'].encode("utf-8"),item['balance'],item['balanceunit'].encode("utf-8"))
        items.append(item)
        sql = 'insert into haijinsuo_product_info(productname,amount,amountunit,annualrate,term,termunit,balance,balanceunit) values( %s,%s,%s,%s,%s,%s,%s,%s)'
        par = values
        prductName = "".join(item['productName'])
        a = self.conn.find_product(prductName,'haijinsuo_product_info')
        if a == 0:
             self.conn.query(sql, par)
        else:
             print '此数据数据库中已存在！'
        return items

    #荷包项目解析函数
    def urls_hb_urls(self, response):
        sel = Selector(response)
        #获取当前列表页中所有在售新标的url跳转链接(a节点)
        product_urls  = sel.xpath('//a[@class="btn_red_little btn_little"]').extract()
        #product_urls  = sel.xpath('//tr[@class="m20r_2w"]/td/font/b/text()').extract()#20个tr
        for product_url in product_urls:
            print product_url
            soup = BeautifulSoup(product_url, 'lxml')
            #https://member.hexindai.com/invest/detail-bid_15722421.html
            newUrls = 'https://member.hexindai.com' + soup.a['href']
            yield scrapy.Request(newUrls, callback = self.parse_cj, encoding = 'utf-8')