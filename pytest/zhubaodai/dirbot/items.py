from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    url = Field()
    description = Field()

class ZBD_Items(Item):

    amount = Field()
    annualRate = Field()
    term = Field()
    proname = Field()
    repaymentMethod = Field()
    minamount = Field()
    proid = Field()

class ZBD_INV_Items(Item):

    rank = Field()
    bidder = Field()
    bidamount = Field()
    validamount = Field()
    bidtime = Field()
    bidmethod = Field()
    proid = Field()