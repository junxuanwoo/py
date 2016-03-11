# -*- coding: utf-8 -*-
'''
__function__: 拾财贷
__auth__: wjx
__date__: 2016-03-09
'''
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
import sys
sys.path.append("../../../../../")
from COMMON.db import DBConn
from COMMON.common import Common
from COMMON.items import ProductItem

class SCD_Spider(Spider):
    #拾财贷
    name = "SCD"
    allowed_domains = ["s.shicaidai.com"]
    conn = DBConn.get_instance()
    common = Common.get_instance()
    #定期赚
    start_urls = common.getUrls('https://s.shicaidai.com/index2/', 1,'.html', '立即认购',0)
    #print start_urls

    def start_requests(self):
        #print self.start_urls
        for url in self.start_urls:
            yield scrapy.Request(url, callback = self.parse_url, encoding='utf-8')

    def parse_url(self, response):
        sel = Selector(response)
        #获取跳转链接
        urls = sel.xpath('//div[@class="fr mr39 mt30"]//a[@id and @href and not(@style)]/@href').extract()
        for url in urls:
            productid = re.search(r'(\w+)\.html', url).group(0).replace('.html','')
            yield scrapy.Request(url, callback = self.parse_scd,
                                 meta={'producturl':url ,'productid':productid},
                                 encoding='utf-8')

    def parse_scd(self, response):
        sel = Selector(response)
        item = ProductItem()

        item['platformid'] = 'P00612'# 平台ID
        item['producttype'] = '定期赚'# 产品类型
        item['startdate'] = item['enddate'] = ''
        item['producturl'] = response.meta['producturl'] # 产品url
        item['productname'] = sel.xpath('//h1[@class="font19ATB"]/text()').extract()[0].strip() # 产品名称
        item['productid'] = response.meta['productid']# 产品ID
        item['amount'] = sel.xpath('//div[@id="AboutToBeginTableA"]/span/text()').extract()[0]
        item['balance'] = sel.xpath('//span[@id="other_accountmoney"]/text()').extract()[0]
        item['minrate'] = item['maxrate'] = sel.xpath('//div[@class="sel_nianhuax "]/span/span[@id="yrtId"]/text()').extract()[0]
        item['term'] = sel.xpath('//div[@class="sel_qixianhx "]/span/span[@id="qxId"]/text()').extract()[0]
        item['termunit'] = sel.xpath('//div[@class="sel_qixianhx "]/span/span[@class="sel_font12"]/text()').extract()[0].strip()
        repaymentmethod = sel.xpath('//div[@class="sel_huahkuanx"]/span/text()').extract()
        for r in repaymentmethod:
            result = r.strip()
            if len(result) > 1:
               item['repaymentmethod'] = result
        # print item['platformid'],item['producturl'],item['productid'],item['productname'],item['producttype'],\
        #    item['amount'],item['balance'],item['term'],item['maxrate'],item['termunit'],item['repaymentmethod']

        recv = self.conn.find_product(item['platformid'], item['productid'])
        if recv:
            # 存在便更新余额
            self.conn.update(item['balance'], item['platformid'], item['productid'])
        else:
            # 不存在便插入新标
            self.conn.insert(item)
