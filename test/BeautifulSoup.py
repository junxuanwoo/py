#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re

html_doc = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
    <body>
        <p class="title"><b>The Dormouse's story</b></p>
        <p class="story">Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
        and they lived at the bottom of a well.</p>
        <p class="story">...</p>
"""

html_doc2 = """
<a href="/invest/a521.html" class="buy">立即投资</a>
"""

#soup = BeautifulSoup(html_doc2, "lxml")
#soup.a['href']
#print(soup.prettify)
#regex = re.compile()
#for li in href_list:    
#print soup.find(href="http*")
#str = soup.a(text=True
#)[0].encode("utf-8")
#print str

#newUrl = 'www.haifax.cn' + soup.a['href']
#print newUrl

#money = "￥200000.00"
#print len(money)
#regex = re.compile(r'^\d+\.\d+')
#result = regex.findall(money)
#print result[0]
#print result



a = 'aabbccaa'
reg = re.compile(r'aa')
bn = reg.findall(a)
print bn



