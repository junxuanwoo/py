# -*- coding: utf-8 -*-
#楚天财富网

from scrapy.spiders import Spider
from scrapy.selector import Selector
from webCrawler.items import CTCF_product
from Common.common import common_getUrls
from DBHelper.DBHelper import DBConn
#from bs4 import BeautifulSoup

class CTCF_Spider(Spider):
    #楚天财富
    name = "CTCF"
    allowed_domains = ["https://www.hbctcf.com/"]
    #楚天财富的散标投资url
    #https://www.hbctcf.com/financing/sbtz/index.html
    common_getUrls()
    start_urls = "https://www.hbctcf.com/financing/sbtz/"

    def parse(self, response):
        pass
        # sel = Selector(response)
        # items = []
        # values = []
        # item = CTCF_product()
        # product =sel.xpath('//div[@class="fn-clear  mb25"]/dl')
        #
        # item['amount'] = product[0].xpath('dd/em/text()')[0].extract().encode("utf-8")
        # item['annualRate'] = product[1].xpath('dd/em/text()')[0].extract().encode("utf-8")
        # item['term'] = product[2].xpath('dd/em/text()')[0].extract().encode("utf-8")
        # item['safeguard']=sel.xpath('//span[@class="fn-left basic-value last"]/text()')[0].extract().encode("utf-8")
        # item['prepaymentRate']=sel.xpath('//span[@class="fn-left basic-value num"]/em/text()')[0].extract().encode("utf-8")
        # item['repaymentMethod']=sel.xpath('//span[@class="fn-left basic-value"]/text()')[0].extract().encode("utf-8")
        # item['proid'] = response.url.split("loanId=")[1]
        # values.append([item['amount'], item['annualRate'], item['term'], item['safeguard'], item['prepaymentRate'], item['repaymentMethod'], '', '', '', item['proid']])
        # items.append(item)
        #
        # try:
        #     conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
        #     cur=conn.cursor()
        #     conn.select_db('product_info')
        #     cur.executemany('insert into renrendai(amount, annualRate, term, safeguard,prepaymentRate, repaymentMethod, progress,remainingTime,balance, proid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', values)
        #     conn.commit()
        #     cur.close()
        #     conn.close()
        # except MySQLdb.Error:
        #     print '数据库操作异常！'
        #
        # return items
