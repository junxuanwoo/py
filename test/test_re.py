#coding=utf-8

import sys,os
import re

def getS():
    str = '大夫山 12-324'
    s = str.split(" ")
    print s[1]
    #regex = re.compile(r'\w+')
    #result = regex.findall(str)
    #print result

getS()
