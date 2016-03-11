# -*- coding: utf-8 -*-
'''
__function__: PPmoney
__auth__: wjx
__date__: 2016-03-11
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

class PPmoney_Spider(Spider):
    # PPmoney
    name = "PPmoney"
    allowed_domains = ["www.ppmoney.com"]
    conn = DBConn.get_instance()
    common = Common.get_instance()
    regex = re.compile(r'\d+')
    #TODO:定期理财,计划理财2个type
    start_urls = common.getUrls('http://www.ppmoney.com/touzilicai/#Page=', 1, '&orderby=-1&isPublic=true', '立即投资', 2)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_url, encoding='utf-8')

    def parse_url(self, response):
        # 获取在售新标的url
        sel = Selector(response)
        urls = sel.xpath('//a[@class="mai-btn"]/@href').extract()
        for url in urls:
            # #判断是否为新手标
            is_new = sel.xpath('//a[@href="{}"]/@title'.format(url)).extract()[0]
            if "新手" in is_new:
                continue
            newUrl = 'https://www.irongbei.com{}'.format(url)
            yield scrapy.Request(newUrl, callback=self.parse_rbw,
                                 meta={'producturl': newUrl, 'productname': is_new},
                                 encoding='utf-8')

    def parse_rbw(self, response):
        sel = Selector(response)
        item = ProductItem()

        item['platformid'] = 'P00622'  # 平台ID
        item['producttype'] = re.search(ur"[\u4e00-\u9fa5]+", response.meta['productname']).group(0) # 产品类型
        item['producturl'] = response.meta['producturl']
        item['productname'] = response.meta['productname']# 产品名称
        item['productid'] = self.regex.search(item['producturl']).group(0)  # 产品ID
        infos = sel.xpath('//font[@class="sz1"]/text()').extract()
        item['amount'] = int(infos[0])*10000# 总额
        item['minrate'] = infos[1]
        item['startdate'] = ''
        item['enddate'] = ''
        item['maxrate'] = item['minrate']
        balance = sel.xpath('//div[@class="jdsm f_14"]/p/font/text()').extract()[0]
        item['balance'] = ''.join(self.regex.findall(balance))
        item['term'] = sel.xpath('//font[@class="sz1 z08"]/text()').extract()[0]# 期限
        item['termunit'] = sel.xpath('//font[@class=" z24"]/text()').extract()[0]# 还款期限单位
        item['repaymentmethod'] = sel.xpath('//font[@class="z z20"]/text()').extract()[1]# 还款方式

        # print item['platformid'],item['producturl'],item['productid'],item['productname'],item['producttype'],\
        #    item['amount'],item['balance'],item['term'],item['maxrate'],item['termunit'],item['repaymentmethod']
        recv = self.conn.find_product(item['platformid'], item['productid'])
        if recv:
            # 存在便更新余额
            self.conn.update(item['balance'], item['platformid'], item['productid'])
        else:
            # 不存在便插入新标
            self.conn.insert(item)
