#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.spiders import Spider
from dirbot.items import WSD_REC_Items
import xml.dom.minidom
import MySQLdb

class WSDSpider(Spider):

    #温商贷
    name = "WSD_REC"
    allowed_domains = ["wsloan.com"]
    start_urls = []
    minId=10776
    maxId=10777
    for i in range(minId, maxId):
        url = "http://www.wsloan.com/biaojs.aspx?act=tbjl&id=%d" % (i)
        start_urls.append(url)

    def parse(self, response):
        items = []
        values = []
        item = WSD_REC_Items()

        DOMTree = xml.dom.minidom.parseString(response.body_as_unicode().strip().split("<script>")[0])
        Data = DOMTree.documentElement
        trs = Data.getElementsByTagName("tr")
        for tr in trs:
            item['num'] = tr.getElementsByTagName("td")[0].childNodes[0].childNodes[0].data
            item['bidder'] = tr.getElementsByTagName("td")[1].childNodes[0].data
            item['bidamount'] = tr.getElementsByTagName("td")[2].childNodes[0].childNodes[0].data
            item['bidtime'] = tr.getElementsByTagName("td")[3].childNodes[0].data
            item['interest'] = tr.getElementsByTagName("td")[4].childNodes[0].childNodes[0].data
            item['source'] = ''
            item['proid'] = response.url.split("id=")[1]
            values.append([item['num'], item['bidder'], item['bidamount'], item['bidtime'], item['interest'], item['source'], item['proid']])
            items.append(item)

        try:
            conn=MySQLdb.connect(host='192.168.0.212', user='root', passwd='abc123,./', port=3306, charset='utf8')
            cur=conn.cursor()
            conn.select_db('product_info')
            cur.executemany('insert into wsloan_inv(num, bidder, bidamount, bidtime, interest, source, proid) values(%s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error:
            print '数据库操作异常！'

        return items
