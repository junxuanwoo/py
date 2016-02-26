#coding=utf-8

from scrapy.spiders import Spider
from dirbot.items import TBCT_Items
import json
import MySQLdb

class TBCTSpider(Spider):

    #腾邦创投
    name = "TBCT"
    allowed_domains = ["p2p178.com"]
    start_urls = []
    minId= 22000
    maxId= 22954
    for i in range(minId, maxId):
        url = "http://www.p2p178.com/api/OPTSDBT3/OPTS308006.dow?RSP_AJX=true&PRG_SEND_ID=0000000%d" % (i)
        start_urls.append(url)

    # start_urls = ['http://www.p2p178.com/api/OPTSDBT3/OPTS308006.dow?RSP_AJX=true&PRG_SEND_ID=000000022554']

    def parse(self, response):
        python_obj = json.loads(response.body_as_unicode())
        items = []
        values = []
        item = TBCT_Items()

        item['amount'] = python_obj.get('PRG_APY_AMT').encode('utf-8')
        item['annualRate'] = python_obj.get('PRG_APY_AMT').encode('utf-8')
        item['term'] = python_obj.get('CI_FEE').encode('utf-8')
        item['proname']=python_obj.get('PRG_NM').encode('utf-8')
        item['usages']=python_obj.get('PRG_USE').encode('utf-8')
        item['endtime']=python_obj.get('INVEST_END_TM').encode('utf-8')
        item['repaydate']=python_obj.get('EXPIRYDT').encode('utf-8')
        item['proid'] = response.url.split("PRG_SEND_ID=")[1]
        values.append([item['amount'], item['annualRate'], item['term'], item['proname'], item['usages'], item['endtime'], item['repaydate'], item['proid']])
        items.append(item)

        try:
            conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
            cur=conn.cursor()
            conn.select_db('product_info')
            cur.executemany('insert into p2p178(amount, annualRate, term, proname,usages, endtime, repaydate, proid) values(%s, %s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            print '数据库操作异常！'

        return items
