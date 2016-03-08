from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    url = Field()
    description = Field()

class RRD_product(Item):

    amount = Field()
    annualRate = Field()
    term = Field()
    safeguard = Field()
    prepaymentRate = Field()
    repaymentMethod = Field()
    progress = Field()
    remainingTime = Field()
    balance = Field()
    proid = Field()

class PPJJ_product(Item):

    amount = Field()
    annualRate = Field()
    term = Field()
    safeguard = Field()
    prepaymentRate = Field()
    repaymentMethod = Field()
    progress = Field()
    remainingTime = Field()
    balance = Field()

class LXJR_Items(Item):

    amount = Field()
    annualRate = Field()
    term = Field()
    repaymentMethod = Field()
    usages = Field()
    proname = Field()
    maxamount = Field()
    minamount = Field()

class TBCT_Items(Item):

    amount = Field()
    annualRate = Field()
    term = Field()
    proname = Field()
    usages = Field()
    endtime = Field()
    repaydate = Field()

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


