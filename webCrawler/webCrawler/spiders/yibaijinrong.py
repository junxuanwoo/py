# -*- coding: utf-8 -*-
#一百金融
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
from webCrawler.spiders.db import DBConn
from webCrawler.items import ProductItem
from bs4 import BeautifulSoup

class YBJR_Spider(Spider):
    #一百金融
    name = "YBJR"

    def __init__(self):
        #self.name = "YBJR"
        self.allowed_domains = ["www.pp100.com"]
        self.conn = DBConn.get_instance()
        self.regex = re.compile(r'\d+')
        self.start_urls = self.conn.getUrls('https://www.pp100.com/front/invest/investHome?currPage=', 1,'&pageSize=&bidStatus=-1&period=0&apr=0&searchType=0', '还款中')
        print "start_urls = ", self.start_urls

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback = self.get_short_url, encoding = 'utf-8')

    #获取短链接url,并拼接
    def get_short_url(self,response):
        sel = Selector(response)
        product_urls  = sel.xpath('//a[@class="x_investDebt_btn"]').extract() # 获取所有立即投资的a节点
        for product_url in product_urls:
            if len(sel.xpath('//strong[@class="x_invest_Normal"]').extract()): # 有返回值表示非新手标
                soup = BeautifulSoup(product_url, 'lxml')
                #print soup.a['href']
                newUrl = 'https://www.pp100.com' + soup.a['href']
                print newUrl
                yield scrapy.Request(newUrl, callback = self.parse, encoding = 'utf-8')

    def parse(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = ProductItem()

        #nodes  = sel.xpath('//div[@class="newZqInfo"]')
        item['platformid'] = 'P00558'# 平台ID
        proInfo = sel.xpath('//div[@class="xTbInfoBid_t fl"]/h2/text()')[0].extract().encode('utf-8')#去掉首尾空格
        tmp = proInfo.split(' ')#壹商贷   E42016030303
        item['producttype'] = str(tmp[0])# 产品类型
        item['productid'] = str(tmp[1])#产品ID
        #print  '--',item['producttype'],'--',item['productid'],'--'
        item['productname'] = item['producttype'] + item['productid']  # 产品名称
        #TODO:没有去掉空格因为编码问题
        proInfo = sel.xpath('//div[@class="xTbInfoBid_cont"]/div/p/text()').extract() # 获取3个信息
        item['amount'] = proInfo[0]# 标的总额(元)
        item['maxrate'] = proInfo[1].strip()# 最大收益率(%)
        item['minrate'] = proInfo[1].strip()# 最小收益率(%)
        item['term'] = proInfo[2] # 还款期限
        print item['amount'], item['maxrate'], item['term']
        item['balance'] = sel.xpath('//div[@class="operate_cash xTb_cash"]/p/i/text()')[0].extract() #标的余额(元)
        item['startdate'] = 'NO' # 产品发标时间
        item['enddate'] = 'NO'# 产品结标时间
        proInfo = sel.xpath('//div[@class="xTbInfoBid_cont"]/div/p/i/text()').extract()
        item['termunit'] = proInfo[0][-1]# 还款期限单位
        proInfo = sel.xpath('//div[@class="xTbInfoBid_word"]/div/p/text()').extract()
        item['repaymentmethod'] = str(proInfo[1]).replace(r'：', '') # 还款方式

        values = (item['platformid'],item['producttype'],item['productname'].encode('utf-8'),item['productid'],item['amount'].encode('utf-8'),
                  item['balance'].encode('utf-8'),item['maxrate'].encode('utf-8'),item['minrate'].encode('utf-8'),
                  item['startdate'].encode('utf-8'),item['enddate'],item['term'],item['termunit'].encode('utf-8'),item['repaymentmethod'].encode('utf-8'))
        items.append(item)
        sql = 'insert into newbid_product_info_test1(platformid,producttype,productname,productid,amount,balance,maxrate,minrate,' \
              'startdate,enddate,term,termunit,repaymentmethod) values( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        par = values
        a = self.conn.find_product(item['platformid'], item['productid'])
        if a == 0:
            self.conn.query(sql, par)
        else:
            print '此数据数据库中已存在！'
        return items

