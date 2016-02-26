#coding=utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import ZBD_Items
import MySQLdb

class ZBDSpider(Spider):

    #珠宝贷
    name = "ZBD"
    allowed_domains = ["zhubaodai.com"]
    # start_urls = []
    # minId=804000
    # maxId=804472
    # for i in range(minId, maxId):
    #     url = "http://www.we.com/lend/detailPage.action?loanId=%d" % (i)
    #     start_urls.append(url)

    start_urls = ['https://secure.zhubaodai.com/investmentDetail/investmentDetails/nview.do?ln_no=JK16020211283742']

    def parse(self, response):
        sel = Selector(response)
        items = []
        values = []
        item = ZBD_Items()

        item['amount'] = sel.xpath('//div[@class="element rightBorder totalMoney"]/p/text()')[1].extract().encode("utf-8").strip()
        item['annualRate'] = sel.xpath('//div[@class="element rightBorder"]/p/text()')[1].extract().encode("utf-8")
        item['term'] = sel.xpath('//div[@class="element rightBorder"]/p/text()')[3].extract().encode("utf-8").strip()
        item['proname']=sel.xpath('//dt[@class="row-fluid bao"]/text()')[0].extract().encode("utf-8").strip()
        item['repaymentMethod']=sel.xpath('//div[@class="element repay"]/p/text()')[1].extract().encode("utf-8")
        item['minamount']=sel.xpath('//div[@class="element rightBorder w33"]/p/em/text()')[0].extract().encode("utf-8").replace('元','')
        item['proid'] = response.url.split("ln_no=")[1]
        values.append([item['amount'], item['annualRate'], item['term'], item['proname'], item['repaymentMethod'], item['minamount'], item['proid']])
        items.append(item)

        try:
            conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
            cur=conn.cursor()
            conn.select_db('product_info')
            cur.executemany('insert into zhubaodai(amount, annualRate, term, proname,repaymentMethod, minamount, proid) values(%s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            print '数据库操作异常！'

        return items
