#coding=utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import LXJR_Items
import MySQLdb

class LXJRSpider(Spider):

    #前海理想金融
    name = "LXJR"
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
        item = LXJR_Items()


        item['amount'] = sel.xpath('//div[@id="subject_lower_l"]/table/tr')[1].xpath('td/text()')[0].extract().encode("utf-8").replace('￥','')
        item['annualRate'] = sel.xpath('//div[@id="subject_lower_l"]/table/tr')[1].xpath('td/text()')[1].extract().encode("utf-8")
        item['term'] = sel.xpath('//div[@id="subject_lower_l"]/table/tr')[1].xpath('td/text()')[1].extract().encode("utf-8")
        item['proname']=sel.xpath('//div[@id="sh_boxm"]/ol/li/h1/text()')[0].extract().encode("utf-8")
        item['usages']=sel.xpath('//div[@id="subject_lower_l"]/table/tr')[2].xpath('td/span/text()')[2].extract().encode("utf-8")
        item['minamount']=sel.xpath('//div[@id="subject_lower_l"]/table/tr')[3].xpath('td/span/text()')[0].extract().encode("utf-8").replace('元','')
        item['maxamount']=sel.xpath('//div[@id="subject_lower_l"]/table/tr')[3].xpath('td/span/text()')[1].extract().encode("utf-8")
        item['repaymentMethod']=sel.xpath('//div[@id="subject_lower_l"]/table/tr')[2].xpath('td/span/text()')[0].extract().encode("utf-8")
        item['proid'] = response.url.split("/")[4].replace('.html','')
        values.append([item['amount'], item['annualRate'], item['term'], item['proname'], item['usages'], item['minamount'], item['maxamount'], item['repaymentMethod'], item['proid']])
        items.append(item)

        try:
            conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
            cur=conn.cursor()
            conn.select_db('product_info')
            cur.executemany('insert into id68(amount, annualRate, term, proname,usages, minamount,maxamount, repaymentMethod, proid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            print '数据库操作异常！'

        return items
