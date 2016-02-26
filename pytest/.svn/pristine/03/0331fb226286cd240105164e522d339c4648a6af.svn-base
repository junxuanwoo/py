#coding=utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import HXD_RP_Items
import MySQLdb

class HXD_REPAYSpider(Spider):

    #和信贷_还款计划
    name = "HXD_REPAY"
    allowed_domains = ["hexindai.com"]

    # start_urls = []
    # minId=460000
    # maxId=500000
    # for i in range(minId, maxId):
    #     url = "https://member.hexindai.com/invest/detail-bid_%d.html" % (i)
    #     start_urls.append(url)

    start_urls=['https://member.hexindai.com/invest/repayplan-bid_468952-forPackage_0-pageid_1.html']

    def parse(self, response):
        sel = Selector(response)
        items = []
        values = []
        item = HXD_RP_Items()
        products =sel.xpath('//div[@class="box_tbl"]/table/tbody/tr')
        for product in products:
            item['period'] = product.xpath('td/text()')[0].extract().encode("utf-8")
            item['repaydate'] = product.xpath('td/text()')[1].extract().encode("utf-8")
            item['repaytotal'] = product.xpath('td/text()')[2].extract().encode("utf-8")
            item['principal'] = product.xpath('td/text()')[3].extract().encode("utf-8")
            item['interest'] = product.xpath('td/text()')[4].extract().encode("utf-8")
            item['status'] = product.xpath('td')[5].xpath('span/span/text()')[0].extract().encode("utf-8")
            item['loannum'] = sel.xpath('//span[@class="loan_id"]/text()')[0].extract().encode("utf-8").replace('借款编号：','')
            values.append([item['period'], item['repaydate'], item['repaytotal'], item['principal'], item['interest'], item['status'], item['loannum']])
            items.append(item)

        conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
        cur=conn.cursor()
        conn.select_db('product_info')
        try:
            conn.begin()
            cur.executemany('insert into hxd_repayplan(period, repaydate, repaytotal, principal,interest,status,loannum) values(%s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            conn.rollback()
            print '数据库操作异常！'
        return items
