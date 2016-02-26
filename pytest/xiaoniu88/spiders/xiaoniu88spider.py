# coding=utf-8
import re
from string import strip
import scrapy
import urllib, re
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from xiaoniu88.settings import HEADERS, COOKIES

#小牛在线做了防爬处理,在cookie中加了一个标识：
#'sr':'334.127.201.43.11.3.119.130.184.156.0.33.20.15.07'
#请求的时候，带上cookie,并在cookie中加上上面这行的代码，就行了
#所有的请求都要带上，要不然就会被重定向走
# 要爬取的产品：
# 1.安心牛
# 2.散标系列
# 3.月月牛
# 4.天天牛
# 5.富盈人生
from DBHelper.XNDBHelper import DBConn


class gscfSpider(CrawlSpider):
    name = "xnrun"
    allowed_domains = ["www.xiaoniu88.com"]
    start_urls = []
    conn = DBConn.get_instance()
    #小牛在线每个产品只放30页到页面上，所以只能爬取这30页的内容
    url_ax = "http://www.xiaoniu88.com/product/planning/"  # 安心牛第一页
    url_sb = "http://www.xiaoniu88.com/product/listing/"  # 散标系列第一页
    url_zr = "http://www.xiaoniu88.com/product/transfer/"  # 转让系列第一页
    url_fy = "http://www.xiaoniu88.com/product/treasure/"  # 富盈人生第一页


    def start_requests(self):
        # url_prefix = 'http://www.xiaoniu88.com/product/planning/detail/247'
        # for i in range(909,1000):
        #     strI = str(i)
        #     if i < 10 :
        #         strI = '00' + str(i)
        #     if i < 100 :
        #         strI = '0' + str(i)
        #     url = url_prefix + strI
        #     yield scrapy.Request(url,callback=self.parse_tmp, headers=HEADERS,cookies=COOKIES,encoding='utf-8')
        for i in range(1,31):
            url_curr_ax = self.url_ax + str(i)
            url_curr_sb = self.url_sb + str(i)
            url_curr_zr = self.url_zr + str(i)+'/0-0/0-0-0-0'
            url_curr_fy = self.url_fy + str(i)
            yield scrapy.Request(url_curr_ax, callback=self.parse_id_ax, headers=HEADERS,cookies=COOKIES,encoding='utf-8')
            yield scrapy.Request(url_curr_sb, callback=self.parse_id_sb, headers=HEADERS,cookies=COOKIES,encoding='utf-8')
            yield scrapy.Request(url_curr_zr, callback=self.parse_id_zr, headers=HEADERS,cookies=COOKIES,encoding='utf-8')
            yield scrapy.Request(url_curr_fy, callback=self.parse_id_fy, headers=HEADERS,cookies=COOKIES,encoding='utf-8')
    # def parse_tmp(self,response):
    #     self.conn.save_url(response.url)

    def parse_id_ax(self,response):
        objList = []
        sel = Selector(response)
        obj = sel.xpath('//span[@class="til"]//a[contains(@href, "/product/planning/detail/")]/@href')
        for item in obj:
            tupleTmp = (item.extract().encode("utf-8"),"AX")
            objList.append(tupleTmp)
        self.conn.save_url(objList)

    def parse_id_sb(self,response):
        objList = []
        sel = Selector(response)
        obj = sel.xpath('//span[@class="til"]//a[contains(@href, "/product/listing/detail/")]/@href')
        for item in obj:
            tupleTmp = (item.extract().encode("utf-8"),"SB")
            objList.append(tupleTmp)
        self.conn.save_url(objList)

    def parse_id_zr(self,response):
        objList = []
        sel = Selector(response)
        obj = sel.xpath('//span[@class="til"]//a[contains(@href, "/product/transfer/detail/")]/@href')
        for item in obj:
            tupleTmp = (item.extract().encode("utf-8"),"ZR")
            objList.append(tupleTmp)
        self.conn.save_url(objList)

    def parse_id_fy(self,response):
        objList = []
        sel = Selector(response)
        obj = sel.xpath('//span[@class="til"]//a[contains(@href, "/product/treasure/detail/")]/@href')
        for item in obj:
            tupleTmp = (item.extract().encode("utf-8"),"FY")
            objList.append(tupleTmp)
        self.conn.save_url(objList)