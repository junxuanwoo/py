# -*- coding: utf-8 -*-
'''
__function__: 梧桐理财
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

class WTLC_Spider(Spider):
    #梧桐理财
    name = "WTLC"
    allowed_domains = ["www.91wutong.com"]
    conn = DBConn.get_instance()
    common = Common.get_instance()
    #随心投
    start_urls = common.getUrls('http://www.91wutong.com/pts/product/products.htm?transfer=0&qidian=0'
                                '&status=0&youhui=0&leftday=0&discount_money=0&page=',0, '', '马上投资')
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
            yield scrapy.Request(url, callback = self.parse_sxt,
                                 meta={'producturl': url}, encoding='utf-8')

    def parse_sxt(self, response):
        sel = Selector(response)
        item = ProductItem()

        item['platformid'] = 'P00608'# 平台ID
        item['producttype'] = '随心投'# 产品类型
        item['producturl'] = response.meta['producturl']
        item['productname'] = sel.xpath('//div[@class="fl bold t2"]/text()').extract()[0] # 产品名称
        item['productid'] = re.search(r'\d+', item['productname']).group(0)# 产品ID
        info = sel.xpath('//div[@class="mb-sm-3 invest_total"]/text()').extract()[0]
        result = re.findall(r'\d+', info)
        item['amount'] = int(result[0])*10000
        item['balance'] = int(result[1])*10000
        item['minrate'] = item['maxrate'] = sel.xpath('//div[@class="wd-100 f50 text-primary number"]/text()').extract()[0]
        item['startdate'] = sel.xpath('//div[@class="wd-33 fl text-left"]/text()').extract()[0]
        item['enddate'] = sel.xpath('//div[@class="wd-33 fl text-center"]/text()').extract()[0].strip()
        item['term'] = sel.xpath('//div[@class="wd-21 fl pl-4"]/div[@class="wd-100 f50 number"]/text()').extract()[0].strip()
        item['termunit'] = sel.xpath('//div[@class="wd-21 fl pl-4"]/div[@class="wd-100 f50 number"]/span/text()').extract()[0].strip()
        item['repaymentmethod'] = sel.xpath('//div[@class="wd-34 fl text-right"]/span/../text()').extract()[1].strip()

        #print item['platformid'],item['producturl'],item['productid'],item['productname'],item['producttype'],\
        #   item['amount'],item['balance'],item['term'],item['maxrate'],item['termunit'],item['repaymentmethod']
        recv = self.conn.find_product(item['platformid'], item['productid'])
        if recv:
            # 存在便更新余额
            self.conn.update(item['balance'], item['platformid'], item['productid'])
        else:
            # 不存在便插入新标
            self.conn.insert(item)
