from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    url = Field()
    description = Field()

class SYD_Items(Item):

    amount = Field()
    annualRate = Field()
    term = Field()
    repaymentMethod = Field()
    membercount = Field()
    proname = Field()
    proid = Field()