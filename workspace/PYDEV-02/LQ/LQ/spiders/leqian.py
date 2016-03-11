# -*- coding: utf-8 -*-
'''
__function__: 乐钱
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

class LQ_Spider(Spider):
    # 乐钱
    name = "LQ"
    allowed_domains = ["www.leqian.com"]
    conn = DBConn.get_instance()
    common = Common.get_instance()
    regex = re.compile(r'\d+')
    start_urls = common.getUrls('https://www.leqian.com/invest/list-', 1, '.html', '立即投资', 0)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_url, encoding='utf-8')

    def parse_url(self, response):
        # 获取在售新标的url
        sel = Selector(response)
        urls = sel.xpath('//a[@class="btn"]/@href').extract()
        for url in urls:
            newUrl = 'https://www.leqian.com{}'.format(url)
            yield scrapy.Request(newUrl, callback=self.parse_rbw,
                                 meta={'producturl': newUrl},
                                 encoding='utf-8')

    def parse_rbw(self, response):
        sel = Selector(response)
        item = ProductItem()

        item['platformid'] = 'P00657'  # 平台ID
        #TODO:类型为图标需要知道全部属性代表什么类型
        item['producttype'] = '乐钱投资' # 产品类型
        item['producturl'] = response.meta['producturl']
        item['productname'] = sel.xpath('//h1/span[not(@class)]/text()').extract()[0]# 产品名称
        item['productid'] = self.regex.search(item['producturl']).group(0)  # 产品ID
        amount = self.regex.search(sel.xpath('//div[@class="field-amount"]/p/text()').extract()[0].strip()).group(0)
        item['amount'] = int(amount)*10000 # 总额
        item['balance'] = sel.xpath('//div[@class="field-amount"]/div/span[@id="reAmount"]/text()').extract()[0].replace(r',', '')
        rate = self.regex.findall(sel.xpath('//div[@class="field-rate"]/p/text()').extract()[0].strip())
        if int(rate[1]) == 0:
            item['minrate'] = item['maxrate'] = rate[0]  # 最大/小利率
        else:
            item['maxrate'] = rate[1]  # 最大利率
            item['minrate'] = rate[0]  # 最小利率
        item['startdate'] = item['enddate'] = ''
        info = sel.xpath('//div[@class="field-term"]/p/text()').extract()[0]# 期限
        item['term'] = self.regex.search(info).group(0)
        item['termunit'] = info[-1]# 还款期限单位
        item['repaymentmethod'] = sel.xpath('//div[@class="fields-col"]/div[@class="field"]/text()[1]').extract()[0].strip()# 还款方式

        recv = self.conn.find_product(item['platformid'], item['productid'])
        if recv:
            # 存在便更新余额
            self.conn.update(item['balance'], item['platformid'], item['productid'])
        else:
            # 不存在便插入新标
            self.conn.insert(item)
