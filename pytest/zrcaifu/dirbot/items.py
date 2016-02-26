from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    url = Field()
    description = Field()

class ZRCF_Items(Item):

    amount = Field()
    annualRate = Field()
    term = Field()
    proname = Field()
    prostatus = Field()
    memcount = Field()
    safeguard = Field()
    repaymentMethod = Field()
    publdate = Field()
    repaydate = Field()
    proid = Field()

class ZRCF_INV_Items(Item):

    amount = Field()
    annualRate = Field()
    term = Field()
    proname = Field()
    prostatus = Field()
    memcount = Field()
    safeguard = Field()
    repaymentMethod = Field()
    publdate = Field()
    repaydate = Field()
    proid = Field()