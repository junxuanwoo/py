# coding=utf-8
from string import strip
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from DB.DBHelper import DBConn
#从数据库里拿到已抓取的最大的产品ID(idMaxStock)与页面上的最大的产品ID(idMaxPage)比较
#抓取idMaxStock与idMaxPage之间的产品
#保存抓取的产品到数据库
from Local_Items import GscfItem, GscfBorrowerInfo, GscfBorrowerAuthInfo, GscfInvestRecords


class gscfSpider(CrawlSpider):
    name = "gscfrun"
    allowed_domains = ["www.goodsure.cn"]
    start_urls = []
    id_Max_Stock = 0
    conn = DBConn.get_instance()
    error_code = 0
    objPrdInfo = None
    objBorrower = None
    objAuthInfo = None
    objInvestRecs = None

    #抓取先前取到数据库中最大的产品ID(id_Max_Stock)
    def __init__(self):
        self.id_Max_Stock = self.conn.get_last_id()


    def start_requests(self):
        url = "http://www.goodsure.cn/invest_list/main.html?limit_type=0&borrow_type=5&status_type=0&page=1&times=1"
        yield scrapy.Request(url, callback=self.parse_getMaxId_xinshoubiao)

    #先抓取新手标的最大产品ID号
    def parse_getMaxId_xinshoubiao(self, response):
        #产品列表的长度
        idList = response.xpath('//span[@class="span3 fl pl15 nowrap"]/a/@href')
        lenList = len(idList)
        idMax = 0
        for i in range(0, lenList):
            idTmp = int(idList[i].extract().replace('/invest/', '').replace('.html', ''))
            if idTmp > idMax:
                idMax = idTmp

        url = "http://www.goodsure.cn/invest_list/main.html?limit_type=0&borrow_type=6&status_type=0&page=1&times=1"
        yield scrapy.Request(url, callback=self.parse_getMaxId_weixinbiao, meta={"idMax": idMax})

    #再抓取微信标的最大产品ID号,与新手标的最大产品ID号比较，取大的那个
    def parse_getMaxId_weixinbiao(self, response):
        idMax = response.meta["idMax"]
        #产品列表的长度
        idList = response.xpath('//span[@class="span3 fl pl15 nowrap"]/a/@href')
        lenList = len(idList)
        for i in range(0, lenList):
            idTmp = int(idList[i].extract().replace('/invest/','').replace('.html', ''))
            if idTmp > idMax:
                idMax = idTmp
        url = "http://www.goodsure.cn/invest_list/main.html?limit_type=0&borrow_type=7&status_type=0&page=1&times=1"
        yield scrapy.Request(url, callback=self.parse_getMaxId_tuijianbiao, meta={"idMax":idMax})

    #再抓取推荐标的最大产品ID号,与新手标跟微信标的大者比较，取大的那个，最终的ID号就是平台最大的产品ID号
    def parse_getMaxId_tuijianbiao(self, response):
        idMax = response.meta["idMax"]
        #产品列表的长度
        idList = response.xpath('//span[@class="span3 fl pl15 nowrap"]/a/@href')
        lenList = len(idList)
        for i in range(0, lenList):
            idTmp = int(idList[i].extract().replace('/invest/', '').replace('.html', ''))
            if idTmp > idMax:
                idMax = idTmp
        for idParse in range(9637, 9638):
        # for idParse in range(self.id_Max_Stock+1, idMax+1):
            prifix = "http://www.goodsure.cn/invest/"
            endfix = ".html"
            url = prifix + str(idParse) + endfix
            yield scrapy.Request(url, callback=self.parse_item_info, meta={"prdid":idParse})

    #保存所有信息
    def parse_item_info(self, response):
        prdid = response.meta["prdid"] # 产品编号
        sel = Selector(response)
        self.objPrdInfo = self.get_product_info(sel,prdid)  # 产品明细
        self.objBorrower = self.get_borrower_info(sel) # 借款人信息
        self.objAuthInfo = self.get_borrower_auth_info(sel) # 借款人认证信息
        self.objInvestRecs = self.get_invest_records(response) # 投资记录
        self.conn.save_all_info_to_db(self.objPrdInfo,self.objBorrower,self.objAuthInfo,self.objInvestRecs)

    # 产品明细
    def get_product_info(self,sel,prdid):
        objItem = GscfItem
        itemPrdName = sel.xpath('//h3[@class="p15 invset-info-title ti10"]/text()') #获取产品名称+产品编号
        itemMortgage = sel.xpath('//div[@class="mortgage-tips"]/p/text()') #抵押物说明
        itemBorrower = sel.xpath('//div[@class="guarantee-tips"]/p/text()') #借款人编号
        itemBorrowAmountList = sel.xpath('//span[@class="span5 f30 bold"]/text()') #借款金额
        itemBorrowAmountUnitList = sel.xpath('//span[@class="span5 f30 bold"]/em/text()') #借款金额单位
        itemBorrowRateList = sel.xpath('//span[@class="span4 f30 bold"]/text()') #年利率
        itemBorrowRateUnitList = sel.xpath('//span[@class="span4 f30 bold"]/em/text()') #年利率单位
        itemBorrowDueLimitList = sel.xpath('//span[@class="span3 f30 bold"]/text()') #借款期限
        itemBorrowDueLimitUnitList = sel.xpath('//span[@class="span3 f30 bold"]/em/text()') #借款期限单位
        itemList1 = sel.xpath('//li[@class="fn-clear border-gray h60 row-fluid ti10"]//span[@class="fl span7"]//span[@class="fl span5"]/text()') #发布时间，最大投标额
        itemList2 = sel.xpath('//li[@class="fn-clear border-gray h60 row-fluid ti10"]//span[@class="fl span5"]//span[@class="fl"]/text()') #还款方式,预期收益
        itemList3 = sel.xpath('//li[@class="fn-clear h60 row-fluid ti10"]//span[@class="fl span5"]//span[@class="fl"]/text()') #借款类型
        ##########--------分割线---------###########
        itemPrdNameList = strip(itemPrdName[0].extract().encode('utf-8')).split("-")
        objItem.pfno = "P000002"
        objItem.prdid = prdid
        objItem.prdname = itemPrdNameList[0]
        objItem.prdno = itemPrdNameList[1]
        objItem.hasmortgage = itemMortgage[0].extract().encode("utf-8")
        borrowerList = itemBorrower[0].extract().encode("utf-8").split("：")
        objItem.borrower = borrowerList[1]
        objItem.borrowamount = int(itemBorrowAmountList[0].extract().encode("utf-8").replace('￥','').replace(",",""))
        objItem.borrowamountunit =  itemBorrowAmountUnitList[0].extract().encode("utf-8")
        objItem.borrowrate = itemBorrowRateList[0].extract().encode("utf-8")
        objItem.borrowrateunit = itemBorrowRateUnitList[0].extract().encode("utf-8")
        objItem.borrowduelimit = itemBorrowDueLimitList[0].extract().encode("utf-8")
        objItem.borrowduelimitunit = itemBorrowDueLimitUnitList[0].extract().encode("utf-8")
        objItem.publishtime = itemList1[0].extract().encode('utf-8').rstrip().lstrip() # 发布时间
        objItem.maxinvestamount = itemList1[1].extract().encode('utf-8') #最大投资限额
        objItem.repaymenttype = itemList2[1].extract().encode('utf-8') #还款方式
        objItem.expected = itemList2[2].extract().encode('utf-8') #预期收益
        objItem.borrowtype = itemList3[0].extract().encode('utf-8')#借款类型
        return objItem
    # 个人信息
    def get_borrower_info(self,sel):
        objBorrower = GscfBorrowerInfo
        itemListBorrowerInfo = sel.xpath('//div[@class="container_10 fn-clear"]\
                                      //div[@class="grid_10 box mt20 pb20"]/ul//li\
                                      //span[@class="span2"]/text()')
        objBorrower.sex = itemListBorrowerInfo[0].extract().encode("utf-8")
        objBorrower.age = itemListBorrowerInfo[1].extract().encode("utf-8")
        objBorrower.education = itemListBorrowerInfo[2].extract().encode("utf-8")
        objBorrower.marry = itemListBorrowerInfo[3].extract().encode("utf-8")
        objBorrower.incomerange = itemListBorrowerInfo[4].extract().encode("utf-8")
        objBorrower.housing = itemListBorrowerInfo[5].extract().encode("utf-8")
        objBorrower.hascar = itemListBorrowerInfo[6].extract().encode("utf-8")
        objBorrower.industry = itemListBorrowerInfo[7].extract().encode("utf-8")
        objBorrower.unpaid = itemListBorrowerInfo[8].extract().encode("utf-8")
        objBorrower.sumborrowamount = itemListBorrowerInfo[9].extract().encode("utf-8")
        objBorrower.successcount = itemListBorrowerInfo[10].extract().encode("utf-8")
        objBorrower.repaymentcount = itemListBorrowerInfo[11].extract().encode("utf-8")
        objBorrower.overduecount = itemListBorrowerInfo[12].extract().encode("utf-8")
        return objBorrower

    #借款详情
    def get_borrower_auth_info(self,sel):
        objAuth = GscfBorrowerAuthInfo
        itemListBorrowInfo = sel.xpath('//div[@class="container_10 fn-clear mt20 "]\
                                    //div[@class="grid_10 box invset-box-line row-fluid pb20"]\
                                    //ul//span/text()')
        objAuth.authhascar = self.chage_date_format(itemListBorrowInfo[1].extract().encode("utf-8"))
        objAuth.authother = self.chage_date_format(itemListBorrowInfo[3].extract().encode("utf-8"))
        objAuth.authid = self.chage_date_format(itemListBorrowInfo[5].extract().encode("utf-8"))
        objAuth.authmortgage = self.chage_date_format(itemListBorrowInfo[7].extract().encode("utf-8"))
        objAuth.authdomicile = self.chage_date_format(itemListBorrowInfo[9].extract().encode("utf-8"))
        objAuth.autoworked = self.chage_date_format(itemListBorrowInfo[11].extract().encode("utf-8"))
        return objAuth

    # 投标记录
    def get_invest_records(self,response):
        investList = []
        itemList = response.xpath('//div[@class="container_10 fn-clear"]\
                               //div[@class="grid_10 box mt20 pb20"]\
                               /ul\
                               /li[@class="border-gray h40 table-list-item row-fluid tender-item "]')
        for invest in itemList:
            objInvestRecs = GscfInvestRecords
            itemList = invest.xpath("./span/text()")
            objInvestRecs.investseq =  itemList[0].extract().encode("utf-8")
            objInvestRecs.investuser =  itemList[1].extract().encode("utf-8")
            objInvestRecs.investamount =  itemList[2].extract().encode("utf-8")
            objInvestRecs.investtime =  itemList[3].extract().encode("utf-8")
            objInvestRecs.investstatus =  itemList[4].extract().encode("utf-8")
            investList.append(objInvestRecs)
        return investList

    def chage_date_format(self,strDate):
        newDate = ""
        if (strDate <> '-'):
            newDate = strDate
        return newDate

    def _log_page(self, item, filename):
        with open(filename, 'w') as f:
            f.write("%s\n" % item)






















