# -*- coding: utf-8 -*-
#可溯贷
import scrapy
from scrapy.selector import Selector
from scrapy.spider import Spider
from DBHelper1 import DBConn
from KSD.items import KSD_product
from bs4 import BeautifulSoup

class KSD_Spider(Spider):
    #可溯贷
    name = "KSD"
    allowed_domains = ["dai.kesucorp.com"]
    conn = DBConn.get_instance()
    start_urls = conn.getUrls('https://dai.kesucorp.com/project/list?&page=', 1, '', '立即投资')
    print "start_urls = ", start_urls

    def parse(self, response):
        sel = Selector(response)
        #获取当前列表页中所有在售新标的url跳转链接
        product_urls  = sel.xpath('//div/a[@class="btn_d btn_href"]').extract()
        #print product_urls
        for product_url in product_urls:
            soup = BeautifulSoup(product_url, 'lxml')
            newUrl = soup.a['href']
            print "newUrl = ", newUrl
            yield scrapy.Request(newUrl, callback = self.parse_id_fy, encoding = 'utf-8')

    def parse_id_fy(self, response):
        #print response.body_as_unicode()
        print "------------------------------------"
        sel = Selector(response)
        items, values = [], ()
        item = KSD_product()

        item['productName'] = sel.xpath('//div[@class="t_d_c_topbar"]/text()')[0].extract()#产品名称'
        item['amount'] = sel.xpath('//li[@class="t_c_topbar_detail t_c_topbar_detail_last"]/span/text()')[0].extract()#标的总额(万元)
        item['balance'] = sel.xpath('//div[@class="tip_d_t_topbar"]/span/text()')[0].extract()#可投金额(元)
        item['term'] = sel.xpath('//li[@class="t_c_topbar_detail"]/span/text()')[0].extract()#期限(月)
        item['annualRate'] = sel.xpath('//li[@class="t_c_topbar_detail"]/span/text()')[1].extract()#年利率(%)

        item['amountunit'] = '万元'
        item['termunit'] = '月'
        item['balanceunit'] = '元'
        #item['createtime'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        values = (item['productName'].encode("utf-8"),item['amount'],item['amountunit'].encode("utf-8"),
                  item['annualRate'],item['term'], item['termunit'].encode("utf-8"),item['balance'],item['balanceunit'].encode("utf-8"))
        items.append(item)
        sql = 'insert into kesudai_product_info(productname,amount,amountunit,annualrate,term,termunit,balance,balanceunit) values( %s,%s,%s,%s,%s,%s,%s,%s)'
        par = values
        prductName = "".join(item['productName'])
        a = self.conn.find_product(prductName,'kesudai_product_info')
        if a == 0:
            self.conn.query(sql, par)
        else:
            print '此数据数据库中已存在！'
        return items



# # -*- coding: utf-8 -*-
# #可溯贷
#
# import re
# import urllib2
# import scrapy
# from scrapy.selector import Selector
# from scrapy.spider import Spider
# from DBHelper1 import DBConn
# from KSD.items import KSD_product
# from bs4 import BeautifulSoup
#
# def getUrls(leftUrl, minId, rightUrl, flagWord):
#     #循环判断url集合新标产品最大页数
#     urls = []
#     regex = re.compile(flagWord)
#     while (1):
#         url = leftUrl + str(minId) + rightUrl
#         html = urllib2.urlopen(url).read()
#         if (regex.search(html)):
#         #匹配到flagWord标记
#             urls.append(url)
#             minId += 1
#         else:
#             break
#     return urls
#
# class KSD_Spider(Spider):
#     #可溯贷
#     name = "KSD"
#     allowed_domains = ["dai.kesucorp.com"]
#     conn = DBConn.get_instance()
#     start_urls = getUrls('https://dai.kesucorp.com/project/list?&page=', 1, '', '立即投资')
#     print "start_urls = ", start_urls
#
#     def start_requests(self):
#        for url in self.start_urls:
#             response = urllib2.urlopen(url)
#             print response
#             sel = Selector(response)
#             #获取当前列表页中所有在售新标的url跳转链接
#             product_urls  = sel.xpath('//div/a[@class="btn_d btn_href"]').extract()
#             #print product_urls
#             for product_url in product_urls:
#                 soup = BeautifulSoup(product_url, 'lxml')
#                 newUrl = soup.a['href']
#                 print "newUrl = ", newUrl
#                 yield scrapy.Request(newUrl, callback = self.parse_id_fy, encoding = 'utf-8')
#                 # yield scrapy.Request(url_curr_ax, callback=self.parse_id_ax, headers=HEADERS,cookies=COOKIES,encoding='utf-8')
#
#     # def parse(self, response):
#     #     sel = Selector(response)
#     #     #获取当前列表页中所有在售新标的url跳转链接
#     #     product_urls  = sel.xpath('//div/a[@class="btn_d btn_href"]').extract()
#     #     #print product_urls
#     #     for product_url in product_urls:
#     #         soup = BeautifulSoup(product_url)
#     #         newUrl = soup.a['href']
#     #         print "newUrl = ", newUrl
#     #         scrapy.Request(newUrl, callback = self.parse_id_fy, encoding = 'utf-8')
#
#     def parse_id_fy(self, response):
#         #print response.body_as_unicode()
#         print "------------------------------------"
#         sel = Selector(response)
#         items, values = [], ()
#         item = KSD_product()
#
#         item['productName'] = sel.xpath('//div[@class="t_d_c_topbar"]/text()')[0].extract()#产品名称'
#         item['amount'] = sel.xpath('//li[@class="t_c_topbar_detail t_c_topbar_detail_last"]/span/text()')[0].extract()#标的总额(万元)
#         item['balance'] = sel.xpath('//div[@class="tip_d_t_topbar"]/span/text()')[0].extract()#可投金额(元)
#         item['term'] = sel.xpath('//li[@class="t_c_topbar_detail"]/span/text()')[0].extract()#期限(月)
#         item['annualRate'] = sel.xpath('//li[@class="t_c_topbar_detail"]/span/text()')[1].extract()#年利率(%)
#
#         item['amountunit'] = '万元'
#         item['termunit'] = '月'
#         item['balanceunit'] = '元'
#         #item['createtime'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
#
#         values = (item['amount'], item['balance'], item['productName'].encode("utf-8"), item['term'],item['annualRate'],
#                   item['amountunit'].encode("utf-8"), item['termunit'].encode("utf-8"), item['balanceunit'].encode("utf-8"))
#         items.append(item)
#         sql = 'insert into (product_Name,amount,balance, term, annualRate,amountunit,termunit,balanceunit) values( %s,%s,%s, %s, %s,%s,%s,%s)'
#         par = values
#         prductName = "".join(item['productName'])
#         a = self.conn.find_product(prductName,'kesudai_product_info')
#         if a == 0:
#             self.conn.query(sql, par)
#         else:
#             print '此数据数据库中已存在！'
#         return items