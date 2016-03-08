# -*- coding: utf-8 -*-
#种钱网
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
from DBHelper1 import DBConn
from ZQW.items import ZQW_product
from bs4 import BeautifulSoup

class ZQW_Spider(Spider):
    #种钱网
    name = "ZQW"
    allowed_domains = ["www.moneyp2p.cn"]
    conn = DBConn.get_instance()
    regex = re.compile(r'\d+')
    #定存宝
    urls_dcb = conn.getUrls('http://www.moneyp2p.cn/finance.do?curPage=', 1, '&pageSize=10&m=4&title=&paymentMode=&purpose=&raiseTerm=&reward=&arStart=&arEnd=&type=','立即投标')
    #活期宝
    urls_hqb = conn.getUrls('http://www.moneyp2p.cn/finance.do?curPage=',1,'&pageSize=10&m=11&title=&paymentMode=&purpose=&raiseTerm=&reward=&arStart=&arEnd=&type=','立即投标')
    start_urls = []

    def start_requests(self):
        for url in self.urls_dcb:
            yield scrapy.Request(url, callback = self.parse_dcb, encoding = 'utf-8')

        for url in self.urls_hqb:
            yield scrapy.Request(url, callback = self.parse_hqb, encoding = 'utf-8')

    def parse_dcb(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = ZQW_product()

        item['platformid'] = 'P00559'# 平台ID
        item['producttype'] = '定存宝'# 产品类型

        product_urls = sel.xpath('//li/a/div[@class="but_red in_but"]/../..') # 获取立即投标块的产品信息

        for product_url in product_urls:
            item['productname'] = product_url.xpath('.//a[@target="_blank"]/@title').extract()[0] # 产品名称
            href = product_url.xpath('.//a[@target="_blank"]/@href').extract()[0]#产品ID
            item['productid'] = re.findall(r'\d+', href)[-1]
            proInfo = product_url.xpath('.//div[@class="ip_nod ip_nodt"]/ul[not(@class)]/li/text()').extract() # 获取2个信息
            item['startdate'] = ''.join(re.findall(r'[0-9\-]', proInfo[2])) # 产品发标时间
            item['balance'] = ''.join(re.findall(r'[0-9\,\.]', proInfo[4]))#标的余额(元)
            proInfo = product_url.xpath('.//div[@class="ip_nod ip_nodt"]/ul[not(@class)]/li/span/text()').extract()
            item['amount'] = proInfo[0].replace(r'元','')# 标的总额(元)
            item['term'] = ''.join(re.findall(r'\d+',proInfo[1])) # 还款期限
            item['termunit'] = proInfo[1][-1]# 还款期限单位
            rate = product_url.xpath('.//div[@class="ip_pic"]/div/span/p/text()').extract()
            item['maxrate'] = ''.join(re.findall(r'[0-9\.]', rate[0]))# 最大收益率(%)
            item['minrate'] = item['maxrate']# 最小收益率(%)

            values = (item['platformid'],item['producttype'],item['productname'].encode('utf-8'),item['productid'],item['amount'].encode('utf-8'),
                      item['balance'].encode('utf-8'),item['maxrate'].encode('utf-8'),item['minrate'].encode('utf-8'),
                      item['startdate'].encode('utf-8'),item['term'],item['termunit'].encode('utf-8'))
            items.append(item)
            sql = 'insert into newbid_product_info_test1(platformid,producttype,productname,productid,amount,balance,maxrate,minrate,' \
                  'startdate,term,termunit) values( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            par = values
            a = self.conn.find_product(item['platformid'], item['productid'])
            if a == 0:
                self.conn.query(sql, par)
            else:
                print '此数据数据库中已存在！'
            return items

    #TODO:活期宝因为当时没有立即投标未能测试
    def parse_hqb(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = ZQW_product()

        item['platformid'] = 'P00559'# 平台ID
        item['producttype'] = '活期宝'# 产品类型

        product_urls = sel.xpath('//li/a/div[@class="but_red in_but"]/../..') # 获取立即投标块的产品信息

        for product_url in product_urls:
            item['productname'] = product_url.xpath('.//a[@target="_blank"]/@title').extract()[0] # 产品名称
            #print item['productname']#鑫鹏小贷【DC(2016)QBQEADB】
            href = product_url.xpath('.//a[@target="_blank"]/@href').extract()[0]#产品ID
            item['productid'] = re.findall(r'\d+', href)[-1]
            #print  '--',item['producttype'],'--',item['productid'],'--'#-- 定存宝 -- 1257 --
            proInfo = product_url.xpath('.//div[@class="ip_nod ip_nodt"]/ul[not(@class)]/li/text()').extract() # 获取2个信息
            item['startdate'] = ''.join(re.findall(r'[0-9\-]', proInfo[2])) # 产品发标时间
            #item['enddate'] = ''# 产品结标时间
            item['balance'] = ''.join(re.findall(r'[0-9\,\.]', proInfo[4]))#标的余额(元)
            proInfo = product_url.xpath('.//div[@class="ip_nod ip_nodt"]/ul[not(@class)]/li/span/text()').extract()
            item['amount'] = proInfo[0].replace(r'元','')# 标的总额(元)
            item['term'] = ''.join(re.findall(r'\d+',proInfo[1])) # 还款期限
            item['termunit'] = proInfo[1][-1]# 还款期限单位
            #item['repaymentmethod'] = '' # 还款方式

            rate = product_url.xpath('.//div[@class="ip_pic"]/div/span/p/text()').extract()
            item['maxrate'] = ''.join(re.findall(r'[0-9\.]', rate[0]))# 最大收益率(%)
            item['minrate'] = item['maxrate']# 最小收益率(%)
            print item['amount'], item['term'], item['termunit'],item['startdate'],item['maxrate'],item['minrate']

            values = (item['platformid'],item['producttype'],item['productname'].encode('utf-8'),item['productid'],item['amount'].encode('utf-8'),
                      item['balance'].encode('utf-8'),item['maxrate'].encode('utf-8'),item['minrate'].encode('utf-8'),
                      item['startdate'].encode('utf-8'),item['term'],item['termunit'].encode('utf-8'))
            items.append(item)
            sql = 'insert into newbid_product_info_test1(platformid,producttype,productname,productid,amount,balance,maxrate,minrate,' \
                  'startdate,term,termunit) values( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            par = values
            a = self.conn.find_product(item['platformid'], item['productid'])
            if a == 0:
                self.conn.query(sql, par)
            else:
                print '此数据数据库中已存在！'
            return items




