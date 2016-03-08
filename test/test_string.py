#coding=utf-8

import sys,os
import re

def getS():
    #str = '开标时间：2016-03-07'

    #匹配非数字和字母
    #regex = re.compile(r'\W+')
    #
    #result = regex.findall(str)
    #print result[0]

    #匹配数字与-    
    #regex = re.compile(r'[0-9\-]')
    #result = regex.findall(str)
    #print ''.join(result)

    #http://www.91wutong.com/pts/product/product.htm?productid=3976
    str = 'http://www.91wutong.com/pts/product/product.htm?productid=3976'
    regex = re.compile(r'=(\d+)')#匹配出3976
    result = regex.findall(str)
    print result[0]
    
getS()
