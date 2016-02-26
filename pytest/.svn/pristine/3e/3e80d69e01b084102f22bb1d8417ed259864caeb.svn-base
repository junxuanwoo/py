#coding=utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import SYD_Items
import MySQLdb

class WSDSpider(Spider):

    #搜易贷
    name = "SYD"
    allowed_domains = ["souyidai.com"]
    # start_urls = []
    # minId=10000
    # maxId=10700
    # for i in range(minId, maxId):
    #     url = "http://www.wsloan.com/jkxq.aspx?id=%d" % (i)
    #     start_urls.append(url)

    start_urls = ['https://www.souyidai.com/bid/detail/5093360683723']
    def parse(self, response):
        sel = Selector(response)
        items = []
        values = []
        item = SYD_Items()

        item['amount'] = sel.xpath('//div[@class="version-project-list-item list-w150"]/span[@class="version-project-text"]/strong/text()')[0].extract().encode("utf-8").strip()
        item['annualRate'] = sel.xpath('//div[@class="version-project-list-item list-w125"]/span/strong/text()')[0].extract().encode("utf-8")
        item['term'] = sel.xpath('//span[@class="version-project-text"]/span/strong/text()')[0].extract().encode("utf-8")
        item['membercount']=sel.xpath('//div[@class="version-project-cols"]/span/text()')[2].extract().encode("utf-8").strip().replace('人','')
        item['repaymentMethod']=sel.xpath('//span[@class="version-project-text"]/em/text()')[0].extract().encode("utf-8").strip()
        item['proname']=sel.xpath('//div[@class="version-basic-title"]/strong/text()')[0].extract().encode("utf-8")
        item['proid'] = response.url.split("/")[5]
        values.append([item['amount'], item['annualRate'], item['term'], item['membercount'], item['repaymentMethod'], item['proname'], item['proid']])
        items.append(item)

        try:
            conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
            cur=conn.cursor()
            conn.select_db('product_info')
            cur.executemany('insert into souyidai(amount, annualRate, term, membercount, repaymentMethod, proname, proid) values(%s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            print '数据库操作异常！'

        return items
