# -*- coding: utf-8 -*-
#草根投资
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
from DBHelper1 import DBConn
from CGTZ.items import CGTZ_product

class CGTZ_Spider(Spider):
    #草根投资
    name = "CGTZ"
    allowed_domains = ["www.cgtz.com"]
    conn = DBConn.get_instance()
    #优选理财
    start_urls = conn.getUrls('https://www.cgtz.com/projects/t//rate//seq//s/4/rep//c//menu//page/', 1,'.html', '立即投资',0)
    print start_urls
    headers = {
               'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
            }

    def start_requests(self):
        #print self.start_urls
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback = self.parse_url, encoding='utf-8')

    def parse_url(self, response):
        sel = Selector(response)
        #获取跳转链接
        urls = sel.xpath('//dl[@class="bgWhite shadow mb10"]').extract()

        #urls = sel.xpath('//div[@class="fr mr39 mt30"]//a[@id and @href and not(@style)]/@href').extract()
        for url in urls:
            #productid = re.search(r'(\w+)\.html', url).group(0).replace('.html','')
            #print productid
            print url
            #yield scrapy.Request(url, callback = self.parse_scd, meta={'productid':productid}, encoding='utf-8')

    def parse_cgtz(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = CGTZ_product()

        item['platformid'] = 'P00612'# 平台ID
        item['producttype'] = '定期赚'# 产品类型

        item['productname'] = sel.xpath('//h1[@class="font19ATB"]/text()').extract()[0].strip() # 产品名称
        item['productid'] = response.meta['productid']# 产品ID
        item['amount'] = sel.xpath('//div[@id="AboutToBeginTableA"]/span/text()').extract()[0]
        item['balance'] = sel.xpath('//span[@id="other_accountmoney"]/text()').extract()[0]
        item['maxrate'] = sel.xpath('//div[@class="sel_nianhuax "]/span/span[@id="yrtId"]/text()').extract()[0]
        item['minrate'] = item['maxrate']
        item['term'] = sel.xpath('//div[@class="sel_qixianhx "]/span/span[@id="qxId"]/text()').extract()[0]
        item['termunit'] = sel.xpath('//div[@class="sel_qixianhx "]/span/span[@class="sel_font12"]/text()').extract()[0].strip()
        repaymentmethod = sel.xpath('//div[@class="sel_huahkuanx"]/span/text()').extract()
        for r in repaymentmethod:
            result = r.strip()
            if len(result) > 1:
               item['repaymentmethod'] = result
        #print item['maxrate'], item['term'], item['termunit'],item['repaymentmethod']


        values = (item['platformid'], item['producttype'], item['productname'].encode('utf-8'), item['productid'],
                  item['amount'], item['balance'], item['maxrate'].encode('utf-8'),item['minrate'].encode('utf-8'),
                  item['term'], item['termunit'].encode('utf-8'), item['repaymentmethod'].encode('utf-8'))
        items.append(item)
        sql = 'insert into newbid_product_info_test1(platformid,producttype,productname,productid,amount,balance,maxrate,minrate,' \
              'term,termunit,repaymentmethod) values( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        par = values
        a = self.conn.find_product(item['platformid'], item['productid'])
        if a == 0:
            self.conn.query(sql, par)
        else:
            print '此数据数据库中已存在！'
        return items
