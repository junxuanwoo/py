# -*- coding: utf-8 -*-
'''
__function__: 爬虫启动模块
__auth__: wjx
__date__: 2016-03-09
'''
import os
import sys
import time
import threading
#from scrapy import cmdline
from names import spiderNames


#爬虫运行类
class runSpider(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.thread_stop = False
        #获取当前文件的父路径(绝对路径)
        parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #sys.path.insert(0,parentdir)
        #把PYDEV-02路径拼接进去
        tmppath = os.path.join(parentdir, 'PYDEV-02')
        #最后拼接项目路径
        spiderPath = os.path.join(tmppath, self.name)
        print spiderPath
        os.chdir(spiderPath)

    def run(self):
        while not self.thread_stop:
            #cmdline.execute("scrapy crawl {}".format(self.name).split())
            os.system("scrapy crawl {}".format(self.name))
            time.sleep(100)

    def stop(self):
        self.thread_stop = True

#启动爬虫函数
def start():
    #以现有的爬虫项目list循环爬虫
    for name in spiderNames:
        spider = runSpider(name)
        spider.start()

if __name__ == '__main__':
    start()