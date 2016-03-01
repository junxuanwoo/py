#coding=utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import RRD_product
import MySQLdb

class RRDSpider(Spider):

    #人人贷
    name = "RRD"
    allowed_domains = ["we.com"]
    start_urls = []
    minId=804000
    maxId=804472
    for i in range(minId, maxId):
        url = "http://www.we.com/lend/detailPage.action?loanId=%d" % (i)
        start_urls.append(url)
    def parse(self, response):
        sel = Selector(response)
        items = []
        values = []
        item = RRD_product()
        product =sel.xpath('//div[@class="fn-clear  mb25"]/dl')

        item['amount'] = product[0].xpath('dd/em/text()')[0].extract().encode("utf-8")
        item['annualRate'] = product[1].xpath('dd/em/text()')[0].extract().encode("utf-8")
        item['term'] = product[2].xpath('dd/em/text()')[0].extract().encode("utf-8")
        item['safeguard']=sel.xpath('//span[@class="fn-left basic-value last"]/text()')[0].extract().encode("utf-8")
        item['prepaymentRate']=sel.xpath('//span[@class="fn-left basic-value num"]/em/text()')[0].extract().encode("utf-8")
        item['repaymentMethod']=sel.xpath('//span[@class="fn-left basic-value"]/text()')[0].extract().encode("utf-8")
        item['proid'] = response.url.split("loanId=")[1]
        values.append([item['amount'], item['annualRate'], item['term'], item['safeguard'], item['prepaymentRate'], item['repaymentMethod'], '', '', '', item['proid']])
        items.append(item)

        try:
            conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
            cur=conn.cursor()
            conn.select_db('product_info')
            cur.executemany('insert into renrendai(amount, annualRate, term, safeguard,prepaymentRate, repaymentMethod, progress,remainingTime,balance, proid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            print '数据库操作异常！'

        return items
