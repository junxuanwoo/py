# -*- coding: utf-8 -*-

#url链表
urlList = [
    #[allowed_domains,[start_urls],rule_key]
    #当url有出现'&'字符时,必须加'\'转义
    ['www.glyd.cn',['http://www.glyd.cn/invest/index1/post/%255B%255D/p/', 1, '.html', '立即投标', 0], 'glyd', ''],# 格林e贷产品
    #['www.5262.com',['http://www.5262.com/product/list.html?sortby=\&direction=\&page=', 1, '', '立即投资', 0], 'hrjr']# 华人金融(产品类型须自己截取)]
]

name = {

}
#规则文件
#@xpath:xpath字符串表达式
#@ruleIndex:xpath返回值后的取值下标
#@regex:正则表达式字符串
#@split:split()函数参数list
#@replace:replace()函数第一个参数
#@sequence:regex,split,replace执行顺序
productRule = {
    #格林e贷
    'glyd' :{
            'platformid':'P00557',# 平台ID
            'producttype': {
                'xpath':'//div[@class="fxndetail_wrap"]/table/tr/td[@class="fxndetail_wrap_td"]/text()',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 产品类型
            'productname': {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 产品名称
            'productid': {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 产品ID
            'amount': {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 标的总额(元)
            'balance':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 标的余额(元)
            'maxrate':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 最大收益率(%)
            'minrate':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 最小收益率(%)
            'startdate':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 产品发标时间
            'enddate':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 产品结标时间
            'term':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 还款期限
            'termunit':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 还款期限单位
            'repaymentmethod':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 还款方式
        },
    #壹佰金融
    'ybjr' :{
            'platformid':'P00557',# 平台ID
            'producttype': {
                'xpath':'//div[@class="fxndetail_wrap"]/table/tr/td[@class="fxndetail_wrap_td"]/text()',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 产品类型
            'productname': {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 产品名称
            'productid': {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 产品ID
            'amount': {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 标的总额(元)
            'balance':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 标的余额(元)
            'maxrate':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 最大收益率(%)
            'minrate':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 最小收益率(%)
            'startdate':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 产品发标时间
            'enddate':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 产品结标时间
            'term':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 还款期限
            'termunit':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 还款期限单位
            'repaymentmethod':  {
                'xpath':'',
                'ruleIndex':0,
                'regex':False,
                'split':False,
                'replace':False,
                'sequence':False
            },# 还款方式
        }
};

