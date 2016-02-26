from scrapy.item import Item, Field

class Website(Item):

    name = Field()
    url = Field()
    description = Field()

class WSD_Items(Item):

    amount = Field()
    annualRate = Field()
    term = Field()
    starttime = Field()
    repaymentMethod = Field()
    safeguard = Field()
    proname = Field()
    proid = Field()

class WSD_REC_Items(Item):

    num = Field()
    bidder = Field()
    bidamount = Field()
    bidtime = Field()
    interest = Field()
    source = Field()
    proid = Field()