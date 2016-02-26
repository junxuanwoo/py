#coding=utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import LXJR_INV_Items
import MySQLdb

class LXJRSpider(Spider):

    #前海理想金融
    name = "LXJR_INV"
    allowed_domains = ["id68.cn"]
    # start_urls = []
    # minId=804000
    # maxId=804472
    # for i in range(minId, maxId):
    #     url = "http://www.we.com/lend/detailPage.action?loanId=%d" % (i)
    #     start_urls.append(url)

    start_urls = ['http://www.id68.cn/preference/3184.html']

    def parse(self, response):
        sel = Selector(response)
        items = []
        values = []
        item = LXJR_INV_Items()
        trlist= sel.xpath('//div[@id="divInvestDetail"]/table/tr')
        for i in range(1,len(trlist)):
            item['bidder'] = trlist[i].xpath('td/text()')[0].extract().strip()
            item['amount'] = trlist[i].xpath('td/text()')[2].extract().strip().encode("utf-8").replace('元','')
            item['bidtime'] = trlist[i].xpath('td/text()')[3].extract().strip()
            item['bidtype'] = trlist[i].xpath('td/text()')[4].extract().strip()
            item['status'] = trlist[i].xpath('td/span/text()')[0].extract().strip()
            item['proid'] = response.url.split("/")[4].replace('.html','')
            values.append([item['bidder'], item['amount'], item['bidtime'], item['bidtype'], item['status'], item['proid']])
            items.append(item)

        try:
            conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
            cur=conn.cursor()
            conn.select_db('product_info')
            cur.executemany('insert into id68_inv(bidder, amount, bidtime, bidtype,status, proid) values(%s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            print '数据库操作异常！'

        return items
