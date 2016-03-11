# -*- coding: utf-8 -*-
'''
__function__: 种钱网
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

class ZQW_Spider(Spider):
    #种钱网
    name = "ZQW"
    allowed_domains = ["www.moneyp2p.cn"]
    conn = DBConn.get_instance()
    common = Common.get_instance()
    start_urls = []
    regex = re.compile(r'\d+')
    #定存宝
    urls_dcb = common.getUrls('http://www.moneyp2p.cn/finance.do?curPage=', 1,
                              '&pageSize=10&m=4&title=&paymentMode=&purpose=&raiseTerm=&reward=&arStart=&arEnd=&type=','即将发布')
    for url in urls_dcb:
        start_urls.append(url)
    #活期宝
    urls_hqb = common.getUrls('http://www.moneyp2p.cn/finance.do?curPage=',1,
                             '&pageSize=10&m=11&title=&paymentMode=&purpose=&raiseTerm=&reward=&arStart=&arEnd=&type=','立即投标')
    for url in urls_hqb:
        start_urls.append(url)
    def start_requests(self):
        for url in self.start_urls:
            print url
            yield scrapy.Request(url, callback = self.parse_url, encoding = 'utf-8')

    #提取产品跳转链接
    def parse_url(self, response):
        sel = Selector(response)
        urls = sel.xpath('//div[@class="in_project"]/div[@class="ipt"]/a/@href')

    def parse_dcb(self, response):
        sel = Selector(response)
        item = ProductItem()

        item['platformid'] = 'P00559'# 平台ID
        item['producttype'] = '定存宝'# 产品类型

        infos = sel.xpath('//li/a/div[@class="but_red in_but"]/../..') # 获取立即投标块的产品信息
        for info in infos:
            item['productname'] = info.xpath('.//a[@target="_blank"]/@title').extract()[0] # 产品名称
            item['producturl'] = info.xpath('.//a[@target="_blank"]/@href').extract()[0]

            item['productid'] = re.findall(r'\d+', item['producturl'])[-1]#产品ID
            proInfo = info.xpath('.//div[@class="ip_nod ip_nodt"]/ul[not(@class)]/li/text()').extract() # 获取2个信息
            item['startdate'] = ''.join(re.findall(r'[0-9\-]', proInfo[2])) # 产品发标时间
            item['enddate'] = ''
            item['balance'] = ''.join(re.findall(r'[0-9\,\.]', proInfo[4]))#标的余额(元)
            proInfo = info.xpath('.//div[@class="ip_nod ip_nodt"]/ul[not(@class)]/li/span/text()').extract()
            item['amount'] = proInfo[0].replace(r'元','')# 标的总额(元)
            item['term'] = ''.join(re.findall(r'\d+',proInfo[1])) # 还款期限
            item['termunit'] = proInfo[1][-1]# 还款期限单位
            rate = info.xpath('.//div[@class="ip_pic"]/div/span/p/text()').extract()
            item['maxrate'] = ''.join(re.findall(r'[0-9\.]', rate[0]))# 最大收益率(%)
            item['minrate'] = item['maxrate']# 最小收益率(%)
            item['repaymentmethod'] = info.xpath('//div[@class="lso_pd"]/ul/li/text()')[4].extract().replace(r'还款方式：', '')
            print item['platformid'],item['producturl'],item['productid'],item['productname'],item['producttype'],\
                item['amount'],item['balance'],item['term'],item['maxrate'],item['termunit'],item['repaymentmethod']
            return
            recv = self.conn.find_product(item['platformid'], item['productid'])
            if recv:
                # 存在便更新余额
                self.conn.update(item['balance'], item['platformid'], item['productid'])
            else:
                # 不存在便插入新标
                self.conn.insert(item)

    #TODO:活期宝因为当时没有立即投标未能测试
    def parse_hqb(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = ProductItem()

        item['platformid'] = 'P00559'# 平台ID
        item['producttype'] = '活期宝'# 产品类型

        infos = sel.xpath('//li/a/div[@class="but_red in_but"]/../..') # 获取立即投标块的产品信息

        for info in infos:
            item['productname'] = info.xpath('.//a[@target="_blank"]/@title').extract()[0] # 产品名称
            href = info.xpath('.//a[@target="_blank"]/@href').extract()[0]#产品ID
            item['productid'] = re.findall(r'\d+', href)[-1]
            proInfo = info.xpath('.//div[@class="ip_nod ip_nodt"]/ul[not(@class)]/li/text()').extract() # 获取2个信息
            item['startdate'] = ''.join(re.findall(r'[0-9\-]', proInfo[2])) # 产品发标时间
            item['enddate'] = ''# 产品结标时间
            item['balance'] = ''.join(re.findall(r'[0-9\,\.]', proInfo[4]))#标的余额(元)
            proInfo = info.xpath('.//div[@class="ip_nod ip_nodt"]/ul[not(@class)]/li/span/text()').extract()
            item['amount'] = proInfo[0].replace(r'元','')# 标的总额(元)
            item['term'] = ''.join(re.findall(r'\d+',proInfo[1])) # 还款期限
            item['termunit'] = proInfo[1][-1]# 还款期限单位
            #item['repaymentmethod'] = '' # 还款方式

            rate = info.xpath('.//div[@class="ip_pic"]/div/span/p/text()').extract()
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




