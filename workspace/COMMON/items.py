# -*- coding: utf-8 -*-
'''
__function__: 保存抓取数据容器类
__auth__: wjx
__date__: 2016-03-09
'''
from scrapy.item import Item, Field

class ProductItem(Item):
  platformid = Field() # 平台ID
  producttype = Field() # 产品类型
  productname = Field() # 产品名称
  producturl = Field() #产品URL
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