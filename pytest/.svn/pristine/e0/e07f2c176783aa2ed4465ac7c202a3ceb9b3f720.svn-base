#coding=utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import WSD_Items
import MySQLdb

class WSDSpider(Spider):

    #温商贷
    name = "WSD"
    allowed_domains = ["wsloan.com"]
    start_urls = []
    minId=10776
    maxId=10777
    for i in range(minId, maxId):
        url = "http://www.wsloan.com/jkxq.aspx?id=%d" % (i)
        start_urls.append(url)

    def parse(self, response):
        sel = Selector(response)
        items = []
        values = []
        item = WSD_Items()

        item['amount'] = sel.xpath('//li[@class="le1"]/i/text()')[0].extract().encode("utf-8").replace('￥','')
        item['annualRate'] = sel.xpath('//li[@class="le3"]/label/i/text()')[0].extract().encode("utf-8").replace('%','')
        item['term'] = sel.xpath('//li[@class="le2"]/label/i/text()')[0].extract().encode("utf-8")
        item['starttime']=sel.xpath('//div[@class="prod-pl"]/table/tr')[1].xpath('td/text()')[1].extract().encode("utf-8").replace('发布时间：','')
        item['safeguard']=sel.xpath('//div[@class="prod-pl"]/table/tr')[0].xpath('td/span/text()')[0].extract().encode("utf-8")
        item['repaymentMethod']=sel.xpath('//div[@class="prod-pl"]/table/tr')[1].xpath('td/span/text()')[0].extract().encode("utf-8")
        item['proname']=sel.xpath('//div[@class="prod-pl"]/h3/text()')[0].extract().encode("utf-8")
        item['proid'] = response.url.split("id=")[1]
        values.append([item['amount'], item['annualRate'], item['term'], item['starttime'], item['safeguard'], item['repaymentMethod'], item['proname'], item['proid']])
        items.append(item)

        try:
            conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
            cur=conn.cursor()
            conn.select_db('product_info')
            cur.executemany('insert into wsloan(amount, annualRate, term, starttime, safeguard, repaymentMethod, proname, proid) values(%s, %s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            print '数据库操作异常！'

        return items
