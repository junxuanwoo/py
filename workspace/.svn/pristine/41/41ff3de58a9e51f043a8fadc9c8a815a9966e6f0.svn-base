# -*- coding: utf-8 -*-
#招财网
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
from DBHelper1 import DBConn
from ZCW.items import ZCW_product

class ZCW_Spider(Spider):
    #招财网
    name = "ZCW"
    allowed_domains = ["www.zhaocaibank.com"]
    conn = DBConn.get_instance()

    #
    start_urls = conn.getUrls('http://www.zhaocaibank.com/index.php?invest&type=allIndex&page=',
                              1, '', '立即投标', 0)
    #print start_urls

    def start_requests(self):
        #print self.start_urls
        for url in self.start_urls:
            yield scrapy.Request(url, callback = self.parse_url, encoding='utf-8')

    def parse_url(self, response):
        sel = Selector(response)
        #获取跳转链接
        urls = sel.xpath('//li[@class="invest_list_btn"]/a[@class="btnRed"]/@href').extract()
        for url in urls:
            print url
            link = 'http://www.zhaocaibank.com{}'.format(url)
            print link
            yield scrapy.Request(link, callback = self.parse_zcw, encoding='utf-8')

    def parse_zcw(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = ZCW_product()

        item['platformid'] = 'P00604'# 平台ID
        item['producttype'] = '招财网'# 产品类型

        item['productname'] = sel.xpath('//div[@classs="tan_tt"]/div[@class="fleft"]/text()').extract()[0].strip() # 产品名称
        item['productid'] = sel.xpath('//input[@name="id"]/@value').extract()[0]  # 产品ID
        item['amount'] = re.search(r'\d+',sel.xpath('//div[@class="tan_info"]/div/strong[@class="orange"]/text()').extract()[0]).group(0) # 标的总额(元)
        proInfo = sel.xpath('//div[@class="tan_info"]/div/').extract()
        for p in proInfo:
            print p

        return item

        item['startdate'] = ''.join(re.findall(r'[0-9\-]', proInfo[2]))  # 产品发标时间
        item['balance'] = ''.join(re.findall(r'[0-9\,\.]', proInfo[4]))  # 标的余额(元)
        proInfo = sel.xpath('.//div[@class="ip_nod ip_nodt"]/ul[not(@class)]/li/span/text()').extract()
        item['term'] = ''.join(re.findall(r'\d+', proInfo[1]))  # 还款期限
        item['termunit'] = proInfo[1][-1]  # 还款期限单位
        rate = sel.xpath('.//div[@class="ip_pic"]/div/span/p/text()').extract()
        item['maxrate'] = ''.join(re.findall(r'[0-9\.]', rate[0]))  # 最大收益率(%)
        item['minrate'] = item['maxrate']  # 最小收益率(%)


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
