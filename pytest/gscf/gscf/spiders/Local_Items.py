# coding=utf-8
import scrapy

class GscfItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pfno = scrapy.Field()   # 平台编号
    prdname = scrapy.Field()# 产品名称
    prdno = scrapy.Field()  # 产品编号
    prdid = scrapy.Field()  # 产品ID
    hasmortgage = scrapy.Field() # 是否有抵押物
    borrower =scrapy.Field() #借款人
    borrowamount = scrapy.Field() #借款金额
    borrowamountunit =scrapy.Field() #借款金额单位
    borrowrate = scrapy.Field() #借款利率
    borrowrateunit = scrapy.Field() #借款利率单位
    borrowduelimit = scrapy.Field() #借款利率
    borrowduelimitunit = scrapy.Field() #借款利率单位
    publishtime = scrapy.Field() #发布时间
    maxinvestamount = scrapy.Field() #最大投资限额
    repaymenttype = scrapy.Field() # 还款方式
    expected = scrapy.Field()# 预期收益
    borrowtype = scrapy.Field()#借款类型
    begintime = scrapy.Field() #计息开始日
    endtime = scrapy.Field() #计息结束日
    pass

class GscfBorrowerInfo(scrapy.Item):
    #----------------------------------#
    #借款人属性
    #----------------------------------#
    pfno = scrapy.Field()                 	# 平台编号
    borrowerid = scrapy.Field()                	# 借款人ID
    sex = scrapy.Field()                 	# 性 别
    age = scrapy.Field()                	# 年 龄
    education = scrapy.Field()                	# 学历
    marry = scrapy.Field()                	# 婚姻状况
    incomerange = scrapy.Field()                    # 收入范围
    housing = scrapy.Field()                	# 住房条件
    hascar = scrapy.Field()                	# 是否购车
    industry = scrapy.Field()                	# 行业
    unpaid = scrapy.Field()                	# 待还总额(元)
    sumborrowamount = scrapy.Field()                	# 累计借款本金(元)
    successcount = scrapy.Field()                	# 成功借款笔数
    repaymentcount = scrapy.Field()                	# 还清笔数
    overduecount = scrapy.Field()                	# 逾期次数
    pass

class GscfBorrowerAuthInfo(scrapy.Item):
    #----------------------------------#
    #借款人认证信息
    #----------------------------------#
    pfno = scrapy.Field()         #平台编号
    borrowerid = scrapy.Field()   #借款人ID
    authhascar = scrapy.Field()   #购车认证
    authhascartime = scrapy.Field()   #购车认证时间
    authother = scrapy.Field()    #其它材料认证
    authothertime = scrapy.Field()    #其它材料认证时间
    authid = scrapy.Field()       #身份认证
    authidtime = scrapy.Field()       #身份认证时间
    authmortgage = scrapy.Field() #抵押登记
    authmortgagetime = scrapy.Field() #抵押登记时间
    authdomicile = scrapy.Field() #居住地认证
    authdomiciletime = scrapy.Field() #居住地认证时间
    autoworked = scrapy.Field()   #工作认证
    autoworkedtime = scrapy.Field()   #工作认证时间
    pass

class GscfInvestRecords(scrapy.Item):
    #----------------------------------#
    #投标记录
    #----------------------------------#
    pfno = scrapy.Field()                     #平台编号
    prdid = scrapy.Field()                    #产品ID
    investseq = scrapy.Field()                #序号
    investuser   = scrapy.Field()             # 投资用户
    investamount   = scrapy.Field()           # 投资金额
    investtime     = scrapy.Field()           # 投资时间
    investstatus   = scrapy.Field()           # 状态
    pass