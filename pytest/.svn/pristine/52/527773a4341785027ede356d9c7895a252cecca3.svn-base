#coding=utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import ZBD_INV_Items
import json
import MySQLdb

class ZBDSpider(Spider):

    #珠宝贷
    name = "ZBD_INV"
    allowed_domains = ["zhubaodai.com"]
    start_urls = []
    minId=1
    maxId=32
    for i in range(minId, maxId):
        url = "https://secure.zhubaodai.com/investmentDetail/investmentDetails/ajaxIvnList.do?currentPage=%d&ln_no=JK16020211283742" % (i)
        start_urls.append(url)

    # start_urls = ['https://secure.zhubaodai.com/investmentDetail/investmentDetails/ajaxIvnList.do?currentPage=1&ln_no=JK16020211283742']

    def parse(self, response):
        python_obj = json.loads(response.body_as_unicode())
        items = []
        values = []
        item = ZBD_INV_Items()

        for i in range(0,5):
            item['rank'] = python_obj.get('list')[i].get('iNDEX_BID')
            item['bidder'] = python_obj.get('list')[i].get('pET_NM')
            item['bidamount'] = python_obj.get('list')[i].get('bID_AMT')
            item['validamount'] = python_obj.get('list')[i].get('eFF_BID_AMT')
            item['bidtime'] = python_obj.get('list')[i].get('bID_DT')
            item['bidmethod'] = python_obj.get('list')[i].get('bID_TYP')
            item['proid'] = response.url.split("ln_no=")[1]
            values.append([item['rank'], item['bidder'], item['bidamount'], item['validamount'], item['bidtime'], item['bidmethod'], item['proid']])
            items.append(item)

        try:
            conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
            cur=conn.cursor()
            conn.select_db('product_info')
            cur.executemany('insert into zhubaodai_inv(rank, bidder, bidamount,validamount, bidtime, bidmethod, proid) values(%s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            print '数据库操作异常！'

        return items
