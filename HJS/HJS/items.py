# -*- coding: utf-8 -*-
from scrapy.item import Item, Field

#海金所
class HJS_product(Item):
    productName = Field()#产品名称
    amount = Field()#总金额
    annualRate = Field()#年利率
    term = Field()#期限(月,天)
    balance = Field()#剩余金额
    amountunit = Field()#总金额单位
    termunit = Field()#期限单位
    balanceunit = Field()#余额单位