# _*_ coding:utf-8 _*_

#xiaohei.python.seo.call.me:)

#win+python2.7.x

import urllib2
from bs4 import BeautifulSoup



def jd(url):
    page = urllib2.urlopen(url)
    html_doc = page.read()
    soup = BeautifulSoup(html_doc.decode('gb2312','ignore'))
    for i in soup.find_all('div', id="sortlist"):
        one = i.find_all('a')
        two = i.find_all('li')
        print ("%s, %s" % one,two)

jd("http://www.dezhong365.com/invest/index/145/6")