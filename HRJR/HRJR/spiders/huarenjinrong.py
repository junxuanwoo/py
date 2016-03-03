# -*- coding: utf-8 -*-
# 华人金融
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spider import Spider
from DBHelper1 import DBConn
from HRJR.items import HRJR_product
from bs4 import BeautifulSoup


class HRJR_Spider(Spider):
    # 华人金融
    name = "HRJR"
    allowed_domains = ["www.5262.com"]
    conn = DBConn.get_instance()
    start_urls = conn.getUrls('http://www.5262.com/product/list.html?sortby=&direction=&page=', 1, '', '立即投资')
    print "start_urls = ", start_urls

    def parse(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = HRJR_product()
        product_urls = sel.xpath('//div[@class="item-data"]')
        # print product_urls
        regex = re.compile(r'\d+')
        for product_url in product_urls:
            # print product_url
            isPutable = product_url.xpath('./ul/li/p/a[@class="ui-btn btnLink btnLink-buy"]/text()').extract()
            if isPutable[0] == '立即投资':
                # 要做立即投资判断
                product_id = product_url.xpath('./h3/a[@class="proName-link"]/text()')[0].extract()  # 产品名称
                if product_id.find("新手") != -1:
                    continue
                else:
                    pName = product_url.xpath('./h3/a[@class="proName-link"]/text()')[0].extract().strip()  # 产品名称
                    pNode = product_url.xpath('./h3/a[@class="proName-link"]')[0].extract().strip()  # 产品名称ID
                    soup = BeautifulSoup(pNode, 'lxml')
                    url = soup.a['href']
                    pId = regex.findall(url)[0]
                    item['productName'] = pName + pId
                    item['amount'] = product_url.xpath('./ul/li[@class="count"]/p/text()')[0].extract().strip()  # 标的总额(万)
                    item['balance'] = product_url.xpath('./ul/li[@class="surplus"]/span/text()')[0].extract().replace(r'剩余 ￥', '').strip()  # 可投金额(元)
                    item['term'] = product_url.xpath('./ul/li[@class="deadline"]/p/text()')[0].extract().strip().strip()  # 期限
                    item['termunit'] = product_url.xpath('./ul/li[@class="deadline"]/p/em/text()')[0].extract().strip()  # 期限单位
                    item['annualRate'] = product_url.xpath('./ul/li[@class="rate"]/p/em/text()')[0].extract().replace(r'%', '').strip()  # 年利率(%)
                    item['amountunit'] = '万'
                    item['balanceunit'] = '元'

                    values = (item['productName'].encode("utf-8"), item['amount'], item['amountunit'].encode("utf-8"),
                          item['annualRate'], item['term'], item['termunit'].encode("utf-8"), item['balance'],
                          item['balanceunit'].encode("utf-8"))
                    items.append(item)
                    sql = 'insert into huarenjinrong_product_info(productname,amount,amountunit,annualrate,term,termunit,balance,balanceunit) values( %s,%s,%s,%s,%s,%s,%s,%s)'
                    par = values
                    prductName = "".join(item['productName'].strip())
                    a = self.conn.find_product(prductName, 'huarenjinrong_product_info')
                    if a == 0:
                        self.conn.query(sql, par)
                    else:
                        print '此数据数据库中已存在！'
        return items
