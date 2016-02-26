#coding=utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import ZRCF_INV_Items
import MySQLdb

class ZRCFSpider(Spider):

    #中瑞财富
    name = "ZRCF_INV"
    allowed_domains = ["zrcaifu.com"]
    # start_urls = []
    # minId=804000
    # maxId=804472
    # for i in range(minId, maxId):
    #     url = "http://www.we.com/lend/detailPage.action?loanId=%d" % (i)
    #     start_urls.append(url)

    start_urls = ['https://www.zrcaifu.com/invest/detail?id=2553']

    def parse(self, response):
        sel = Selector(response)
        items = []
        values = []
        item = ZRCF_INV_Items()

        # item['amount'] = sel.xpath('//span[@class="pub-list-table pub-border-radius"]')
        # item['annualRate'] = sel.xpath('//div[@class="project-value-detail"]/em/span/text()')[0].extract().encode("utf-8").strip()+sel.xpath('//div[@class="project-value-detail"]/em/text()')[0].extract().encode("utf-8").replace('%','')
        # item['term'] = sel.xpath('//span[@class="big-number"]/text()')[0].extract().encode("utf-8").strip()
        # item['proname']=sel.xpath('//a[@class="left project-name "]/text()')[0].extract().encode("utf-8").strip()
        # item['prostatus']=sel.xpath('//div[@class="project-key-detail key-detail-tworows"]/strong/text()')[0].extract().encode("utf-8")
        # item['memcount']=sel.xpath('//div[@class="project-value-detail key-detail-tworows"]/strong/text()')[0].extract().encode("utf-8").replace('人','')
        # item['safeguard']=sel.xpath('//div[@class="col1"]/p/span/span/text()')[0].extract().encode("utf-8")
        # item['repaymentMethod']=sel.xpath('//div[@class="col1"]/p/span/text()')[0].extract().encode("utf-8")
        # item['publdate']=sel.xpath('//div[@class="col1"]/p/span/text()')[1].extract().encode("utf-8")
        # item['repaydate']=sel.xpath('//div[@class="col1"]/p/span/text()')[2].extract().encode("utf-8")
        # item['proid'] = response.url.split("id=")[1]
        # values.append([item['amount'], item['annualRate'], item['term'], item['proname'], item['prostatus'], item['memcount'],item['safeguard'],item['repaymentMethod'],item['publdate'],item['repaydate'],item['proid']])
        # items.append(item)

        trs= sel.xpath('//table[@class="pub-list-table pub-border-radius"]/tr')
        for tr in trs:
             print tr
             print tr.xpath('/th')[0].extract()

        # try:
        #     conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
        #     cur=conn.cursor()
        #     conn.select_db('product_info')
        #     cur.executemany('insert into zrcaifu(amount, annualRate, term, proname,prostatus, memcount,safeguard,repaymentMethod,publdate,repaydate,proid) values(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)', values)
        #     conn.commit()
        #     cur.close()
        #     conn.close()
        # except MySQLdb.Error:
        #     print '数据库操作异常！'

        return items
