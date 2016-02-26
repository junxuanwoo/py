#coding=utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import HXD_CREDCHAN_Items
import MySQLdb

class HXD_CREDCHANSpider(Spider):

    #和信贷_债权承接记录
    name = "HXD_CREDCHAN"
    allowed_domains = ["hexindai.com"]

    # start_urls = []
    # minId=460000
    # maxId=500000
    # for i in range(minId, maxId):
    #     url = "https://member.hexindai.com/invest/detail-bid_%d.html" % (i)
    #     start_urls.append(url)

    start_urls=['https://member.hexindai.com/invest/transferrecord-bid_468952-forPackage_0.html']

    def parse(self, response):
        sel = Selector(response)
        items = []
        values = []
        item = HXD_CREDCHAN_Items()

        products= sel.xpath('//div[@class="box_tbl"]/table/tbody/tr')
        for product in products:
            item['creditor'] = product.xpath('td/text()')[0].extract().encode("utf-8")
            item['acceptor'] = product.xpath('td/text()')[1].extract().encode("utf-8")
            item['acceptamount'] = product.xpath('td/text()')[2].extract().encode("utf-8")
            item['validamount'] = product.xpath('td/text()')[3].extract().encode("utf-8")
            item['principal'] = product.xpath('td/text()')[4].extract().encode("utf-8")
            item['interest'] = product.xpath('td/text()')[5].extract().encode("utf-8")
            item['accepttime'] = product.xpath('td/text()')[6].extract().encode("utf-8")
            item['loannum'] = sel.xpath('//span[@class="loan_id"]/text()')[0].extract().encode("utf-8").replace('借款编号：','')
            values.append([item['creditor'], item['acceptor'], item['acceptamount'], item['validamount'], item['principal'], item['interest'], item['accepttime'],item['loannum']])
            items.append(item)

        conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
        cur=conn.cursor()
        conn.select_db('product_info')
        try:
            conn.begin()
            cur.executemany('insert into hxd_creditorchange(creditor, acceptor, acceptamount, validamount,principal,interest,accepttime,loannum) values(%s, %s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            conn.rollback()
            print '数据库操作异常！'
        return items
