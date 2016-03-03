#coding=utf-8

import sys,os
import re

def getS():
    str = '新手标（迎新金标）10天投'
    s = str.find("新手")
    if s != -1:
        
        print "you"
    else:
        print "wu"
    #regex = re.compile(r'\w+')
    #result = regex.findall(str)
    #print result

getS()
