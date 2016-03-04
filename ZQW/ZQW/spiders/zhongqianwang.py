# -*- coding: utf-8 -*-
#种钱网
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spider import Spider
from DBHelper1 import DBConn
from ZQW.items import ZQW_product
from bs4 import BeautifulSoup

class ZQW_Spider(Spider):
    #种钱网
    name = "ZQW"
    allowed_domains = ["www.pp100.com"]
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

        product_urls  = sel.xpath('//li/a/div[@class="but_red in_but"]/../..') # 获取立即投标块的产品信息
        for product_url in product_urls:
            print product_url
            item['productname'] = product_url.xpath('./div[@class="ipt"]/a/span/p/text()') # 产品名称


        #item['productid'] = str(tmp[1])#产品ID
        #print  '--',item['producttype'],'--',item['productid'],'--'

        #TODO:没有去掉空格因为编码问题
        # proInfo = sel.xpath('//div[@class="xTbInfoBid_cont"]/div/p/text()').extract() # 获取3个信息
        # item['amount'] = proInfo[0]# 标的总额(元)
        # item['maxrate'] = proInfo[1].strip()# 最大收益率(%)
        # item['minrate'] = proInfo[1].strip()# 最小收益率(%)
        # item['term'] = proInfo[2] # 还款期限
        # #print item['amount'], item['maxrate'], item['term']
        # item['balance'] = sel.xpath('//div[@class="operate_cash xTb_cash"]/p/i/text()')[0].extract() #标的余额(元)
        # item['startdate'] = 'NO' # 产品发标时间
        # item['enddate'] = 'NO'# 产品结标时间
        # proInfo = sel.xpath('//div[@class="xTbInfoBid_cont"]/div/p/i/text()').extract()
        # item['termunit'] = proInfo[0][-1]# 还款期限单位
        # proInfo = sel.xpath('//div[@class="xTbInfoBid_word"]/div/p/text()').extract()
        # item['repaymentmethod'] = str(proInfo[1]).replace(r'：', '') # 还款方式
        #
        # values = (item['platformid'],item['producttype'],item['productname'].encode('utf-8'),item['productid'],item['amount'].encode('utf-8'),
        #           item['balance'].encode('utf-8'),item['maxrate'].encode('utf-8'),item['minrate'].encode('utf-8'),
        #           item['startdate'].encode('utf-8'),item['enddate'],item['term'],item['termunit'].encode('utf-8'),item['repaymentmethod'].encode('utf-8'))
        # items.append(item)
        # sql = 'insert into newbid_product_info_test1(platformid,producttype,productname,productid,amount,balance,maxrate,minrate,' \
        #       'startdate,enddate,term,termunit,repaymentmethod) values( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        # par = values
        # a = self.conn.find_product(item['platformid'], item['productid'])
        # if a == 0:
        #     self.conn.query(sql, par)
        # else:
        #     print '此数据数据库中已存在！'
        # return items

    def parse_hqb(self, response):
        pass




