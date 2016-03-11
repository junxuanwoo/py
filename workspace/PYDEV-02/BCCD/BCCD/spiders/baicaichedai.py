# -*- coding: utf-8 -*-
'''
__function__: 百财车贷
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

class BCCD_Spider(Spider):
    # 百财车贷
    name = "BCCD"
    allowed_domains = ["www.83chedai.com"]
    conn = DBConn.get_instance()
    common = Common.get_instance()

    regex = re.compile(r'\d+')

    start_urls = common.getUrls('https://www.83chedai.com/borrowings?page=', 1, '&size=10', '立即投标')

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_url, encoding='utf-8')

    def parse_url(self, response):
        # 获取在售新标的url
        sel = Selector(response)
        infos = sel.xpath('//div[@class="borrowing clearfix"]')
        for info in infos:
            # #判断是否可投
            is_tz = info.xpath('.//a[@class="btn-primary btn btn-block btn-radius mt10"]/text()').extract()
            if is_tz or is_tz[0] != "立即投标":
                continue
            #判断是否是新手专享
            is_new = info.xpath('.//span[@data-container="body"]/text()')[0].extract()
            if is_new == "新手专享":
                continue
            url = info.xpath('.//a[@class="btn-primary btn btn-block btn-radius mt10"]/@href').extract()[0]
            newUrl = 'https://www.83chedai.com{}'.format(url)
            yield scrapy.Request(newUrl, callback=self.parse_bccd,
                                 meta={'producturl': newUrl}, encoding='utf-8')

    def parse_bccd(self, response):
        sel = Selector(response)
        item = ProductItem()

        item['platformid'] = 'P00619'  # 平台ID
        item['producttype'] = '百财车贷'  # 产品类型
        item['producturl'] = response.meta['producturl']
        item['productname'] = sel.xpath('//div[@class="l-container prj-view"]/nav/em[@class="cur"]/text()').extract()[0] # 产品名称
        item['productid'] = sel.xpath('//input[@name="prj_id"]/@value').extract()[0]  # 产品ID
        balance = sel.xpath('//strong[@class="prj-left-amount"]/text()').extract()[0]
        item['balance'] = balance.replace(r'.', '').replace(r',', '').strip()# 标的余额(元)
        #TODO:账面没有总额
        item['amount'] = '' # 总额
        info = sel.xpath('//section[@class="prj-base l-left"]/div[@class="info-list"]/ul/li/text()').extract()
        item['term'] = self.regex.search((info[1].strip())).group(0)# 项目期限
        item['termunit'] = re.search(ur"[\u4e00-\u9fa5]+", info[1].strip()).group(0)# 产品类型# 还款期限单位
        item['repaymentmethod'] = info[4].strip()# 还款方式
        item['maxrate'] = sel.xpath('//section[@class="prj-base l-left"]/div[@class="rate three"]'
                         '/div[@class="center"]/p[@class="rate-number g-rate-black"]/text()').extract()[0]
        item['minrate'] = item['maxrate']
        item['startdate'] = ''
        item['enddate'] = ''
        #print item['platformid'],item['producturl'],item['productid'],item['productname'],item['producttype'],\
        #   item['amount'],item['balance'],item['term'],item['maxrate'],item['termunit'],item['repaymentmethod']

        recv = self.conn.find_product(item['platformid'], item['productid'])
        if recv:
            # 存在便更新余额
            self.conn.update(item['balance'], item['platformid'], item['productid'])
        else:
            # 不存在便插入新标
            self.conn.insert(item)
