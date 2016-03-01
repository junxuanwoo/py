# -*- coding: utf-8 -*-
from scrapy.item import Item, Field

#汉金所
class HJS_product(Item):
    productName = Field()#产品名称
    amount = Field()#总金额
    annualRate = Field()#年利率
    term = Field()#期限(月,天)
    balance = Field()#剩余金额

#楚天财富网
class CTCF_product(Item):
    productName = Field()#产品名称
    amount = Field()#总金额
    annualRate = Field()#年利率
    term = Field()#期限(月,天)
    balance = Field()#剩余金额

#融和贷
class CTCF_product(Item):
    productName = Field()#产品名称
    amount = Field()#总金额
    annualRate = Field()#年利率
    term = Field()#期限(月,天)
    balance = Field()#剩余金额

#汇付四海
class HFSH_product(Item):
    productName = Field()#产品名称
    amount = Field()#总金额
    annualRate = Field()#年利率
    term = Field()#期限(月,天)
    balance = Field()#剩余金额