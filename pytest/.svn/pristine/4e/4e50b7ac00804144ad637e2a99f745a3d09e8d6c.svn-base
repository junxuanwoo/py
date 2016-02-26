#coding=utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import HXD_Items
import MySQLdb

class HXDSpider(Spider):

    #和信贷
    name = "HXD"
    allowed_domains = ["hexindai.com"]

    # start_urls = []
    # minId=460000
    # maxId=500000
    # for i in range(minId, maxId):
    #     url = "https://member.hexindai.com/invest/detail-bid_%d.html" % (i)
    #     start_urls.append(url)

    start_urls=['https://member.hexindai.com/invest/detail-bid_11579737.html']

    def parse(self, response):
        sel = Selector(response)
        items = []
        values = []
        item = HXD_Items()
        product =sel.xpath('//div[@class="invest_new_left"]/table/tbody/tr/td/em/text()')
        item['amount'] = product[0].extract().encode("utf-8")
        item['annualRate'] = product[1].extract().encode("utf-8")
        item['term'] = product[2].extract().encode("utf-8")
        item['maxamount'] = sel.xpath('//span[@id="bid_money_max"]/text()')[0].extract().encode("utf-8")
        item['minamount'] = sel.xpath('//div[@class="invest_bid_info"]/ul')[2].xpath('li/text()')[2].extract().encode("utf-8").replace('最低出借额：','').replace('元','')
        item['starttime'] = sel.xpath('//div[@class="invest_bid_info"]/ul')[1].xpath('li/text()')[0].extract().encode("utf-8").replace('开标时间：','')
        item['repaymentMethod'] = sel.xpath('//div[@class="invest_bid_info"]/ul')[0].xpath('li/text()')[0].extract().encode("utf-8").replace('还款方式：','')
        item['loannum'] = sel.xpath('//span[@class="loan_id"]/text()')[0].extract().encode("utf-8").replace('借款编号：','')
        values.append([item['amount'], item['annualRate'], item['term'], item['maxamount'], item['minamount'], item['starttime'], item['repaymentMethod'],item['loannum']])
        items.append(item)

        conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
        cur=conn.cursor()
        conn.select_db('product_info')
        try:
            conn.begin()
            cur.executemany('insert into hxd_products(amount, annualRate, term, maxamount,minamount,starttime,repaymentMethod,loannum) values(%s, %s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            conn.rollback()
            print '数据库操作异常！'

        return items
