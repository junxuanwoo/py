# -*- coding: utf-8 -*-
#海投汇
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spider import Spider
from DBHelper1 import DBConn
from HTH.items import HTH_product
from bs4 import BeautifulSoup

class HTH_Spider(Spider):
    #海投汇
    name = "HTH"
    allowed_domains = ["www.htouhui.com"]
    conn = DBConn.get_instance()
    start_urls = conn.getUrls('http://www.haifax.cn/invest/index', 1, '.html', '立即投资')
    print "start_urls = ", start_urls

    def parse(self, response):
        sel = Selector(response)
        #获取当前列表页中所有在售新标的url跳转链接
        product_urls  = sel.xpath('//div[@class="invest_a"]/a').extract()
        for product_url in product_urls:
            print product_url
            soup = BeautifulSoup(product_url, 'lxml')
            #print soup.a(text=True)[0].encode("utf-8")
            if soup.a(text=True)[0].encode("utf-8") == "立即投资":
                #print soup.a['href']
                newUrl = 'http://www.haifax.cn' + soup.a['href']
                #print "newUrl = ", newUrl
                yield scrapy.Request(newUrl, callback = self.parse_id_fy, encoding = 'utf-8')

    def parse_id_fy(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = HTH_product()

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
        sql = 'insert into haitouhui_product_info(productname,amount,amountunit,annualrate,term,termunit,balance,balanceunit) values( %s,%s,%s,%s,%s,%s,%s,%s)'
        par = values
        prductName = "".join(item['productName'])
        a = self.conn.find_product(prductName,'haitouhui_product_info')
        if a == 0:
             self.conn.query(sql, par)
        else:
             print '此数据数据库中已存在！'
        return items

