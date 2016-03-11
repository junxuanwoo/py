# -*- coding: utf-8 -*-
'''
__function__: 华人金融
__auth__: wjx
__date__: 2016-03-09
'''
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spider import Spider
import sys
sys.path.append("../../../../../")
from COMMON.db import DBConn
from COMMON.common import Common
from COMMON.items import ProductItem

class HRJR_Spider(Spider):
    # 华人金融
    name = "HRJR"
    allowed_domains = ["www.5262.com"]
    conn = DBConn.get_instance()
    common = Common.get_instance()
    start_urls = common.getUrls('http://www.5262.com/product/list.html?sortby=&direction=&page=', 1, '', '立即投资', 0)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback = self.parse_url, encoding = 'utf-8')

    #获取需要抓取的新标的跳转链接
    def parse_url(self, response):
        sel = Selector(response)
        urls = sel.xpath('//a[@class="ui-btn btnLink btnLink-buy"]/@href').extract()
        for url in urls:
            #print url
            newUrl = 'http://www.5262.com{}'.format(url)
            yield scrapy.Request(newUrl, callback = self.parse_hrjr,
                                 meta={'producturl': newUrl},encoding = 'utf-8')

    def parse_hrjr(self, response):
        sel = Selector(response)
        item = ProductItem()

        #判断是否是新手标
        isNew = sel.xpath('//div[@class="title fn-c"]/h1/text()').extract()[0]
        if re.search(ur'新手', isNew) is not None:
            return

        item['platformid'] = 'P00555'
        item['producttype'] = '华金投资'
        item['productname'] = sel.xpath('//div[@class="title fn-c"]/h1[@class="fn-l"]/text()')[0].extract() # 产品名称
        print item['productname']
        item['productid'] = sel.xpath('//input[@name="id"]/@value')[0].extract()  # 产品ID
        item['producturl'] = response.meta['producturl']
        infos = sel.xpath('//div[@class="detail-left fn-l"]/ul[@class="fn-c"]/li/p/em/text()').extract()
        item['amount'] = int(re.search(r'\d+',infos[0]).group(0).strip())*10000
        item['minrate'] = item['maxrate'] = infos[1].strip()
        item['term'] = infos[2].strip()
        infos = sel.xpath('//div[@class="detail-left fn-l"]/ul[@class="fn-c"]/li/p/text()').extract()[2]
        item['termunit'] = infos[-1]
        item['startdate'] = item['enddate'] = ''
        infos = sel.xpath('//div[@class="info-list fn-c"]/p[@class="fn-l"]/text()').extract()
        item['repaymentmethod'] = infos[3]
        item['balance'] = re.search(r'\d+', infos[1]).group(0)

        recv = self.conn.find_product(item['platformid'], item['productid'])
        if recv:
            # 存在便更新余额
            self.conn.update(item['balance'], item['platformid'], item['productid'])
        else:
            # 不存在便插入新标
            self.conn.insert(item)
