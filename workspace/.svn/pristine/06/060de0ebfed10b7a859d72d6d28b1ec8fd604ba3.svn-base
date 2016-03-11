# -*- coding: utf-8 -*-
# 种钱网
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
from DBHelper1 import DBConn
from LTZ.items import LTZ_product
from bs4 import BeautifulSoup


class LTZ_Spider(Spider):
    # 种钱网
    name = "LTZ"
    allowed_domains = ["lantouzi.com"]
    conn = DBConn.get_instance()
    regex = re.compile(r'\d+')
    # 懒人计划
    urls_lrjh = conn.getUrls('https://lantouzi.com/project/index?page=', 1, '&size=10', '马上投资')

    start_urls = []

    def start_requests(self):
        for url in self.urls_lrjh:
            yield scrapy.Request(url, callback=self.parse_url, encoding='utf-8')

    def parse_url(self, response):
        # 获取在售新标的url
        sel = Selector(response)
        product_urls = sel.xpath('//a[@class="g-btn g-btn-medium-major"]/@href').extract()
        for url in product_urls:
            yield scrapy.Request(url, callback=self.parse_lrjh, encoding='utf-8')

    def parse_lrjh(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = LTZ_product()

        item['platformid'] = 'P00600'  # 平台ID
        item['producttype'] = '懒人计划'  # 产品类型
        item['productname'] = sel.xpath('//div[@class="l-container prj-view"]/nav/em[@class="cur"]/text()').extract()[0] # 产品名称
        item['productid'] = sel.xpath('//input[@name="prj_id"]/@value').extract()[0]  # 产品ID
        item['balance'] = sel.xpath('//strong[@class="prj-left-amount"]/text()').extract()[0].replace(r'.','').strip()  # 标的余额(元)
        #TODO:账面没有总额
        info = sel.xpath('//section[@class="prj-base l-left"]/div[@class="info-list"]/ul/li/text()').extract()
        item['term'] = info[1].strip()# 项目期限
        item['termunit'] = '天'  # 还款期限单位
        item['repaymentmethod'] = info[4].strip()# 还款方式
        item['maxrate'] = sel.xpath('//section[@class="prj-base l-left"]/div[@class="rate three"]'
                         '/div[@class="center"]/p[@class="rate-number g-rate-black"]/text()').extract()[0]
        item['minrate'] = item['maxrate']

        values = (item['platformid'], item['producttype'], item['productname'].encode('utf-8'), item['productid'],
                  item['balance'].encode('utf-8'), item['term'].encode('utf-8'), item['termunit'].encode('utf-8'),
                  item['repaymentmethod'].encode('utf-8'),item['maxrate'].encode('utf-8'), item['minrate'])
        items.append(item)
        sql = 'insert into newbid_product_info_test1(platformid,producttype,productname,productid,balance,' \
              'term,termunit,repaymentmethod,maxrate,minrate) values( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        par = values
        a = self.conn.find_product(item['platformid'], item['productid'])
        if a == 0:
            self.conn.query(sql, par)
        else:
            print '此数据数据库中已存在！'
        return items
