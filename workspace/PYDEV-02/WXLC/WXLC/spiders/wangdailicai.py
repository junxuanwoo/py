# -*- coding: utf-8 -*-
#网信理财
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
from DBHelper1 import DBConn
from WXLC.items import WXLC_product
from bs4 import BeautifulSoup

class ZCW_Spider(Spider):
    #网信理财
    name = "WXLC"
    allowed_domains = ["www.firstp2p.com"]
    conn = DBConn.get_instance()
    #网贷理财
    url_wdlc = conn.getUrls('http://www.firstp2p.com/deals?p=', 1, '', '投资', 24)
    #专享理财
    #url_zxlc = conn.getUrls('http://www.firstp2p.com/touzi?p=', 1, '', '投资', 23)
    #基金理财 TODO:13有待检验
    #url_jjlc = conn.getUrls('http://www.firstp2p.com/jijin?p=', 1, '', '投资', 13)
    #目前只测试网贷理财
    start_urls = []

    def start_requests(self):
        print self.start_urls
        for url in self.start_urls:
            yield scrapy.Request(url, callback = self.parse_url, encoding='utf-8')

    def parse_url(self, response):
        sel = Selector(response)
        #获取跳转链接
        urls = sel.xpath('//li[@class="invest_list_btn"]/a[@class="btnRed"]').extract()
        for url in urls:
             yield scrapy.Request(url, callback = self.parse_zcw, encoding='utf-8')

    # def parse_drw(self, response):
    #     sel = Selector(response)
    #     items, values = [], ()
    #     item = ZCW_product()
    #
    #     item['platformid'] = 'P00559'# 平台ID
    #     item['producttype'] = '定存宝'# 产品类型
    #
    #     product_urls = sel.xpath('//li/a/div[@class="but_red in_but"]/../..') # 获取立即投标块的产品信息
    #
    #     for product_url in product_urls:
    #         item['productname'] = product_url.xpath('.//a[@target="_blank"]/@title').extract()[0] # 产品名称
    #         href = product_url.xpath('.//a[@target="_blank"]/@href').extract()[0]#产品ID
    #         item['productid'] = re.findall(r'\d+', href)[-1]
    #         proInfo = product_url.xpath('.//div[@class="ip_nod ip_nodt"]/ul[not(@class)]/li/text()').extract() # 获取2个信息
    #         item['startdate'] = ''.join(re.findall(r'[0-9\-]', proInfo[2])) # 产品发标时间
    #         item['balance'] = ''.join(re.findall(r'[0-9\,\.]', proInfo[4]))#标的余额(元)
    #         proInfo = product_url.xpath('.//div[@class="ip_nod ip_nodt"]/ul[not(@class)]/li/span/text()').extract()
    #         item['amount'] = proInfo[0].replace(r'元','')# 标的总额(元)
    #         item['term'] = ''.join(re.findall(r'\d+',proInfo[1])) # 还款期限
    #         item['termunit'] = proInfo[1][-1]# 还款期限单位
    #         rate = product_url.xpath('.//div[@class="ip_pic"]/div/span/p/text()').extract()
    #         item['maxrate'] = ''.join(re.findall(r'[0-9\.]', rate[0]))# 最大收益率(%)
    #         item['minrate'] = item['maxrate']# 最小收益率(%)
    #
    #         values = (item['platformid'],item['producttype'],item['productname'].encode('utf-8'),item['productid'],item['amount'].encode('utf-8'),
    #                   item['balance'].encode('utf-8'),item['maxrate'].encode('utf-8'),item['minrate'].encode('utf-8'),
    #                   item['startdate'].encode('utf-8'),item['term'],item['termunit'].encode('utf-8'))
    #         items.append(item)
    #         sql = 'insert into newbid_product_info_test1(platformid,producttype,productname,productid,amount,balance,maxrate,minrate,' \
    #               'startdate,term,termunit) values( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    #         par = values
    #         a = self.conn.find_product(item['platformid'], item['productid'])
    #         if a == 0:
    #             self.conn.query(sql, par)
    #         else:
    #             print '此数据数据库中已存在！'
    #         return items
