# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#import scrapy


#class LianjinsuoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    pass


from scrapy.item import Item, Field


# class Website(Item):
#
#     name = Field()
#     url = Field()
#     description = Field()

class YYS_product(Item):
    product_name = Field()


class LJTC_product(Item):
    pass

class LJMD_product(Item):
    pass
