from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    url = Field()
    description = Field()

class TBCT_Items(Item):

    amount = Field()
    annualRate = Field()
    term = Field()
    proname = Field()
    usages = Field()
    endtime = Field()
    repaydate = Field()
    proid = Field()

class TBCT_INV_Items(Item):

    invester = Field()
    amount = Field()
    invtime = Field()
    status = Field()
    proid = Field()