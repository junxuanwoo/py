#coding=utf-8
#/usr/bin/python
import sys,os
import re

def getS():
    string = '45天65'
    result = re.search(r'\d+', string)
    if result:
        print result.group(0)
    else:
        print "None"
        
    regex = re.compile(r'\w+')
    for i in result:
        result = regex(string)
    #regex = re.compile(r'\w+')
    #result = regex.findall(str)
    #print result
    

#getS()


ul = ['http://www.glyd.cn/invest/index1/post/%255B%255D/p/', 1, '.html', '立即投标', 0]
url = "{}{}{}".format(ul[0], str(ul[1]), ul[2])
print url
