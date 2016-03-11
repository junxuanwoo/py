# -*- coding: utf-8 -*-
'''
__function__: 海金所
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
from bs4 import BeautifulSoup

class HJS_Spider(Spider):
    #海金所
    name = "HJS"
    allowed_domains = ["www.haifax.cn"]
    conn = DBConn.get_instance()
    common = Common.get_instance()
    start_urls = common.getUrls('http://www.haifax.cn/invest/index', 1, '.html', '立即投资', 0)
    print "start_urls = ", start_urls

    def parse(self, response):
        sel = Selector(response)
        #获取当前列表页中所有在售新标的url跳转链接
        product_urls  = sel.xpath('//div[@class="invest_a"]/a').extract()
        for product_url in product_urls:
            soup = BeautifulSoup(product_url, 'lxml')
            if soup.a(text=True)[0].encode("utf-8") == "立即投资":
                newUrl = 'http://www.haifax.cn' + soup.a['href']
                #print "newUrl = ", newUrl
                yield scrapy.Request(newUrl, callback = self.parse_hjs, meta={'producturl': newUrl}, encoding = 'utf-8')

    def parse_hjs(self, response):
        sel = Selector(response)
        item = ProductItem()

        item['platformid'] = 'P00520' #平台ID
        item['producturl'] = response.meta['producturl'] #产品URL
        item['productid'] = re.search(r'a\d+',item['producturl']).group(0) # 产品ID
        item['productname'] = sel.xpath('//div[@class="biao_con_l_tit"]/h2/text()')[0].extract().strip()#产品名称
        item['producttype'] =  ''.join(re.findall(ur"[\u4e00-\u9fa5]+", item['productname'])) # 产品类型
        total = sel.xpath('//div[@class="biao_con_l_con"]/div[@class="account"]/span/text()')[0].extract()#标的总额(元)
        item['amount'] = re.search(r'\d+', total).group(0)
        item['balance'] = sel.xpath('//div[@class="biao_con_r_con"]/p/text()')[0].extract().replace(r'可投金额：', '')#可投金额(元)
        item['term'] = sel.xpath('//span[@class="time_limit_font"]/text()')[0].extract()#期限
        termunit = sel.xpath('//div[@class="time_limit"]/text()').extract()[2].strip()# 期限单位
        item['termunit'] = termunit[-1]
        item['minrate'] = item['maxrate'] = sel.xpath('//span[@class="apr_font"]/text()')[0].extract().strip()#年利率(%)
        item['startdate'] = item['enddate'] = ''
        item['repaymentmethod'] = sel.xpath('//div[@class="biao_con_l_bot"]/ul/li/span/text()').extract()[2].strip()
        # print item['platformid'],item['producturl'],item['productid'],item['productname'],item['producttype'],\
        #     item['amount'],item['balance'],item['term'],item['maxrate'],item['termunit'],item['repaymentmethod']
        recv = self.conn.find_product(item['platformid'], item['productid'])
        if recv:
            # 存在便更新余额
            self.conn.update(item['balance'], item['platformid'], item['productid'])
        else:
            # 不存在便插入新标
            self.conn.insert(item)