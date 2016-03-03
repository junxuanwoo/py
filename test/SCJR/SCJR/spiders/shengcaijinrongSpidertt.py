#!/usr/bin/python
#-*-coding:utf-8-*-

import scrapy
import MySQLdb
from scrapy.selector import Selector
from scrapy.spider import Spider
import mysql.connector
from DBHelper1 import DBConn

from SCJR.items import ShengcaijinrongItem


class SCJRSpider(Spider):

    name = 'SCJR3'
    allowed_domain=['shengcaijinrong.com']
    start_urls=['https://www.shengcaijinrong.com/bidding/jclist/term0/0/order0/0/status0/0/order_flag0/0/']
    conn = DBConn.get_instance()

    def parse(self, response):
        sel=Selector(response)
        sturl='https://www.shengcaijinrong.com'
        #product=sel.xpath('//div[@class="header_l"]/span[@class="hot_line"]/text()')[0].extract()
        product=sel.xpath('//div[@class="bid_bu"]/a[@href]').extract()
        for item in product:
           newurl= item[9:27]
           url=sturl+newurl
           print  url
           yield scrapy.Request(url, callback=self.parse_id_fy,encoding='utf-8')



    def parse_id_fy(self, response):
        #print response.body_as_unicode()
        sel=Selector(response)
        items=[]
        values=()
        item=ShengcaijinrongItem()



        item['pfno']='P00501'#平台号
        item['ptype']='金财专区'# '产品类型',
        item['prdname']=sel.xpath('//a[@class="nav_default_auto"]/text()').extract()#产品名称',
        item['profit']=sel.xpath('//dl[@class="reveal_dl1"]/dd/span/text()').extract()#年化收益',
        item['repaydate']=sel.xpath('//dl[@class="reveal_dl5s"]/dd/span/text()').extract()#还款期限',
        item['bidAmount']=sel.xpath('//dl[@class="reveal_dl6s"]/dd/text()').extract()#标的总额',
        item['indemnify']=sel.xpath('/html/body/div[5]/div[2]/div[1]/div[1]/div[2]/span[1]/span/text()').extract()#保障方式',
        item['repayTypeName']=sel.xpath('/html/body/div[5]/div[2]/div[1]/div[1]/div[2]/span[2]/text()').extract()#还款方式',
        item['percent']=sel.xpath('//*[@class="numerical-value"]/text()').extract()#募集进度'//
        item['enddate']=sel.xpath('//dd[@class="reveal_bottom_dd state_down"]/text()').extract()#截止天数',
        item['canAmount']=sel.xpath('//span[@class="activity_money"]/text()').extract()#可投金额'
        values = (item['pfno'], item['ptype'], item['prdname'][0].encode("utf-8"), item['profit'][0].encode("utf-8"),
                  item['repaydate'][0].encode("utf-8"),item['bidAmount'][0].encode("utf-8"),
                  item['indemnify'][0].encode("utf-8"),item['repayTypeName'][0].encode("utf-8"),
                  item['percent'][0].encode("utf-8"),item['enddate'][0],item['canAmount'][0].encode("utf-8"))
        items.append(item)

        #sql = 'insert into shengcaijinrong_newbid_info(pfno,ptype,prdname,profit,repaydate,bidAmount,indemnify,repayTypeName,percent,enddate,canAmount) values( %s,%s,%s, %s, %s, %s, %s,%s, %s, %s,%s)'

        sql = 'insert into shengcaijinrong_newbid_info_copy(pfno,ptype,prdname,profit,repaydate,bidAmount,indemnify,repayTypeName,percent,enddate,canAmount) values( %s,%s,%s, %s, %s, %s, %s,%s, %s, %s,%s)'
        par = values
        prductName = "".join(item['prdname'])
        print '------------------', prductName,'------'
        a = self.conn.find_product(prductName,'shengcaijinrong_newbid_info_copy')
        if a == 0:
            self.conn.query(sql, par)
        else:
            print '此数据数据库中已存在！'
        return items




























