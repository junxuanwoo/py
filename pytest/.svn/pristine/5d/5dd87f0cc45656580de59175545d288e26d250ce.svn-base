#coding=utf-8

from scrapy.spiders import Spider
from dirbot.items import TBCT_INV_Items
import json
import MySQLdb

class TBCTSpider(Spider):

    #腾邦创投
    name = "TBCT_INV"
    allowed_domains = ["p2p178.com"]
    start_urls = []
    # minId= 22000
    # maxId= 22954
    # for i in range(minId, maxId):
    #     url = "http://www.p2p178.com/api/OPTSDBT3/OPTS308006.dow?RSP_AJX=true&PRG_SEND_ID=0000000%d" % (i)
    #     start_urls.append(url)

    start_urls = ['http://www.p2p178.com/api/OPTSDBT3/OPTS308012.dow?RSP_AJX=true&PAGEINDEX=1&PAG_NUM=20&PRG_SEND_ID=000000023004']

    def parse(self, response):
        python_obj = json.loads(response.body_as_unicode())
        items = []
        values = []
        item = TBCT_INV_Items()
        reclist = python_obj.get('REC')
        for i in range(0,len(reclist)):
            item['invester'] = python_obj.get('REC')[i].get('USR_OPR_LOG_ID').encode('utf-8')
            item['amount'] = python_obj.get('REC')[i].get('INVEST_AMT')
            item['invtime'] = python_obj.get('REC')[i].get('INVEST_TM')
            item['status']=python_obj.get('REC')[i].get('INVEST_STS')
            item['proid'] = response.url.split("PRG_SEND_ID=")[1]
            values.append([item['invester'], item['amount'], item['invtime'], item['status'], item['proid']])
            items.append(item)

        try:
            conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
            cur=conn.cursor()
            conn.select_db('product_info')
            cur.executemany('insert into p2p178_inv(invester, amount, invtime, status,proid) values(%s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            print '数据库操作异常！'

        return items
