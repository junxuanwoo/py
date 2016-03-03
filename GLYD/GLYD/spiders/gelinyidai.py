# -*- coding: utf-8 -*-
#格林易贷
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spider import Spider
from DBHelper1 import DBConn
from GLYD.items import GLYD_product
from bs4 import BeautifulSoup

class GLYD_Spider(Spider):
    #格林易贷
    name = "GLYD"
    allowed_domains = ["www.glyd.cn"]
    conn = DBConn.get_instance()
    regex = re.compile(r'\d+')
    #格林e宝 http://www.glyd.cn/baobao/index.html
    #格林e贷 http://www.glyd.cn/invest/index1.html?type=1 (目前只有这个是需要抓取的)
    start_urls = conn.getUrls('http://www.glyd.cn/invest/index1/post/%255B%255D/p/', 1, '.html', '立即投标')
    print "start_urls = ", start_urls

    def parse(self, response):
        sel = Selector(response)
        #获取当前列表产品xml模块范围,(没有做是否立即投标判断)
        product_urls  = sel.xpath('//div[@class="fxnbb_inv_r"]')
        for product_url in product_urls:
            #print product_url
            isPutable = product_url.xpath('./div[@class="fxnbb_inv_r_w"]/div[@class="fxnbb_inv_r_w_r"]/em/text()').extract()
            if len(isPutable) > 0 and isPutable[0] == "立即投标":
                localNodes = product_url.xpath('./h3').extract() # 获取到跳转的短链接
                # for i in localNodes:
                #     print i
                soup = BeautifulSoup(localNodes[0], 'lxml')
                localShortUrl = soup.a['href'] # 获取到跳转的短链接
                #print localShortUrl
                localProductId = self.regex.findall(localShortUrl) #获取产品ID
                #print localProductId[0]
                localProductName = soup.span(text=True) # 获取产品名称的第二部分
                #print localProductName
                localStartDate = product_url.xpath('./div[@class="fxnbb_inv_r_w"]/div[@class="fxnbb_inv_r_w_l"]/ul/li/dd/text()')[2].extract() # 获取发标时间
                # for i in localStartDate:
                #     print i
                newUrl = 'http://www.glyd.cn' + localShortUrl
                #print newUrl
                #print "newUrl = %s, productid = %s, localProductName = %s, localStartDatee = %s" % newUrl, localProductId, localProductName, localStartDate[-1]
                yield scrapy.Request(newUrl, callback = self.parse_gled,
                                     meta={'productid': localProductId, 'productname': localProductName, 'startdate': localStartDate},
                                     encoding = 'utf-8')

    #格林e贷产品
    def parse_gled(self, response):
        sel = Selector(response)
        items, values = [], ()
        item = GLYD_product()

        item['platformid'] = 'P00557'# 平台ID
        item['producttype'] = '格林e贷'# 产品类型
        item['productname'] = '格林e贷' + response.meta['productname'][0]# 产品名称
        item['productid'] = response.meta['productid'][0] #产品ID
        localInfo = sel.xpath('//div[@class="fxndetail_wrap"]/table/tr/td/text()').extract() # 获取5个信息
        #print localInfo
        item['amount'] = localInfo[0]# 标的总额(元)
        item['balance'] = sel.xpath('//div[@class="fxndetail_wrap"]/div[@class="fxndetail_wrap_time"]/ul/li/dd[@class="org"]/text()')[1].extract().replace(r'元', '')#标的余额(元)
        item['maxrate'] = localInfo[1].strip()# 最大收益率(%)
        item['minrate'] = localInfo[1].strip()# 最小收益率(%)
        item['startdate'] = response.meta['startdate'] # 产品发标时间
        item['enddate'] = ''# 产品结标时间
        term = self.regex.findall(localInfo[3]) # 还款期限
        item['term'] = term[0]
        item['termunit'] = localInfo[3][-1]# 还款期限单位
        item['repaymentmethod'] = localInfo[2] # 还款方式

        values = (item['platformid'],item['producttype'],item['productname'].encode('utf-8'),item['productid'],item['amount'].encode('utf-8'),
                  item['balance'].encode('utf-8'),item['maxrate'].encode('utf-8'),item['minrate'].encode('utf-8'),
                  item['startdate'].encode('utf-8'),item['enddate'],item['term'],item['termunit'].encode('utf-8'),item['repaymentmethod'].encode('utf-8'))
        items.append(item)
        sql = 'insert into newbid_product_info_test1(platformid,producttype,productname,productid,amount,balance,maxrate,minrate,' \
              'startdate,enddate,term,termunit,repaymentmethod) values( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        par = values
        a = self.conn.find_product(item['platformid'], item['productid'])
        if a == 0:
            self.conn.query(sql, par)
        else:
            print '此数据数据库中已存在！'
        return items

