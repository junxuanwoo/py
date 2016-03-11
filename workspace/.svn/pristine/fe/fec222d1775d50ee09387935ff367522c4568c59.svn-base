# -*- coding: utf-8 -*-
'''
__function__: 九斗鱼
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
from bs4 import BeautifulSoup

class JDY_Spider(Spider):
    # 九斗鱼
    name = "JDY"
    allowed_domains = ["www.9douyu.com"]
    conn = DBConn.get_instance()
    common = Common.get_instance()
    regex = re.compile(r'\d+')
    #九省心
    urls_jsx = common.getUrls('http://www.9douyu.com/invest/project/index/way/creditorNine/p/', 1, '.html', '立即投资', 0)
    #TODO:九安心的html跟省心的获取规则不同
    #urls_jax = common.getUrls('http://www.9douyu.com/invest/project/index/way/factoring/p/', 1, '.html', '立即投资', 0)

    start_urls = urls_jsx

    def start_requests(self):
        producttype = ''
        for url in self.start_urls:
            print url
            if 'creditorNine' in url:
                producttype = '九省心' # 产品类型
            elif 'factoring' in url:
                producttype = '九安心'
            yield scrapy.Request(url, callback=self.parse_url,
                                 meta={'producttype':producttype},
                                 encoding='utf-8')

    def parse_url(self, response):
        # 获取在售新标的url
        sel = Selector(response)
        values = sel.xpath('//a[@class="web-btn 1"]/../..').extract()#获取在售新标的html块
        for v in values:
            soup = BeautifulSoup(v, 'lxml')
            urlstr = soup.li['onclick']
            url = urlstr.split(r'=')[1].replace('\'', '')
            newUrl = 'http://www.9douyu.com{}'.format(url)
            productid = self.regex.search(url).group(0)
            print newUrl, productid
            yield scrapy.Request(newUrl, callback=self.parse_jdy,
                                 meta={'producturl': newUrl, 'productid': productid,
                                       'producttype':response.meta['producttype']},
                                 encoding='utf-8')

    def parse_jdy(self, response):
        sel = Selector(response)
        item = ProductItem()

        item['platformid'] = 'P00658'  # 平台ID
        item['producturl'] = response.meta['producturl']
        item['producttype'] = response.meta['producttype'] # 产品类型
        item['productid'] = response.meta['productid']  # 产品ID
        item['productname'] = sel.xpath('//h4[@class="t-center-title"]/text()').extract()[0].strip().replace(r' ', '')# 产品名称
        infos = sel.xpath('//div[@class="t-center-left-3"]/ul/li/text()').extract()
        item['amount'] = int(self.regex.search(infos[0]).group(0))*10000 # 总额
        item['repaymentmethod'] = infos[1].replace(r'还款方式：', '')# 还款方式
        item['enddate'] = infos[3].replace(r'到期日期：', '')
        balance = sel.xpath('//p[@class="t-center-right-1 t-center-right-mt2"]/text()').extract()[0].replace(r',', '')
        item['balance'] = self.regex.search(balance).group(0)
        infos = sel.xpath('//div[@class="t-center-left-1"]/dl/dt/text()').extract()
        item['minrate'] = item['maxrate'] = infos[0]# 最大/小利率
        item['startdate'] = ''
        item['term'] = self.regex.search(infos[1]).group(0) # 期限
        item['termunit'] = sel.xpath('//div[@class="t-center-left-1"]/dl/dt/span/text()').extract()[1]# 还款期限单位
        print item['productname'],item['productid'],item['amount'],item['balance'], item['enddate'],item['producttype'],\
           item['term'],item['termunit'],item['repaymentmethod']

        recv = self.conn.find_product(item['platformid'], item['productid'])
        if recv:
            # 存在便更新余额
            self.conn.update(item['balance'], item['platformid'], item['productid'])
        else:
            # 不存在便插入新标
            self.conn.insert(item)
