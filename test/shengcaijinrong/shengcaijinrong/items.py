# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field


class ShengcaijinrongItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
  pfno=Field()#平台号
  ptype=Field()# '产品类型',
  prdname=Field()#产品名称',
  profit=Field()#年化收益',
  repaydate=Field()#还款期限',
  bidAmount=Field()#标的总额',
  indemnify=Field()#保障方式',
  repayTypeName=Field()#还款方式',
  percent=Field()#募集进度'
  enddate=Field()#截止天数',
  canAmount=Field()#可投金额',


