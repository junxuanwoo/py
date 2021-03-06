# -*- coding: utf-8 -*-
from scrapy.item import Item, Field

#懒投资
class LTZ_product(Item):
  platformid = Field() # 平台ID
  producttype = Field() # 产品类型
  productname = Field() # 产品名称
  productid = Field() #产品ID
  amount = Field() # 标的总额(元)
  balance = Field() # 标的余额(元)
  maxrate = Field() # 最大收益率(%)
  minrate = Field() # 最小收益率(%)
  startdate = Field() # 产品发标时间
  enddate = Field() # 产品结标时间
  term = Field() # 还款期限
  termunit = Field() # 还款期限单位
  repaymentmethod = Field() # 还款方式