# -*- coding: utf-8 -*-
'''
__function__: 方法功能公用单例类
__auth__: wjx
__date__: 2016-03-09
'''
import re
import urllib2

class Common:
    _instance = None

    def __init__(self):
        pass

    # 静态方法
    @staticmethod
    def get_instance():
        if Common._instance is None:
            Common._instance = Common()
        return Common._instance


    #循环判断url集合新标产品最大页数,并返回需要抓取的平台url
    def getUrls(self,leftUrl, minId, rightUrl, flagWord, count=0):
        urls = []
        regex = re.compile(flagWord)
        while (1):
            url = leftUrl + str(minId) + rightUrl
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            req = urllib2.Request(url, headers = headers)
            #status=urllib.urlopen("http://www.baidu.com").code
            html  = urllib2.urlopen(req).read()
            if len(regex.findall(html)) > count:
                #匹配到flagWord标记
                urls.append(url)
                minId += 1
            else:
                break
        return urls

