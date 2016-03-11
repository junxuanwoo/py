# -*- coding: utf-8 -*-
'''
__function__: 集合爬虫项目需要用到的代码小功能模块
__auth__: wjx
__date__: 2016-03-09
'''

import sys
import threading
import mysql.connector

reload(sys)
sys.setdefaultencoding('utf-8')

# 单例类,只实例化一次
class DBConn:
    _instance = None
    _conn = None
    _cur  = None
    r = None
    mutex = threading.Lock()

    def __init__(self):
        pass
        self._conn =  mysql.connector.connect( host='192.168.0.212',
                                        user='root',
                                        passwd='abc123,./',
                                        db='newbid_product_info',
                                        port=3306,
                                        charset='utf8')

    # 静态方法
    @staticmethod
    def get_instance():
        if DBConn._instance is None:
            DBConn.mutex.acquire()
            if DBConn._instance is None:
                print "1-数据连接组件已创建".encode('utf-8')
                DBConn._instance = DBConn()
            else:
                print "2-无法创建数据连接组件的多个实例".encode('utf-8')
            DBConn.mutex.release()
        return DBConn._instance

    # 提交事务并关闭游标
    def commit_trans(self):
        self._conn.commit()
        self._cur.close()

    # 查询某个平台下某个产品是否存在
    # @return: 存在:1,不存在:0
    # @platformid: 当前平台ID
    # @productid: 当前产品的ID
    def find_product(self, platformid, productid):
        recv = 0
        values = (platformid, productid)
        sql = 'select id from newbid_product_info_table where platformid= %s and productid =%s  limit 1';
        try:
            self._cur = self._conn.cursor()
            self._cur.execute(sql,params=values)
            r = self._cur.fetchone()
            self._cur.close()
            if r is not None:
                recv = 1
        except Exception, e:
            print "3-新标数据库查找数据失败 失败信息为: %s" % e
        return recv

    # 新标数据插入
    # @item:要插入的数据item
    def insert(self,item):
        values = (item['platformid'], item['producttype'], item['productname'], item['producturl'],
                  item['productid'], item['amount'], item['balance'], item['maxrate'],item['minrate'],
                  item['term'], item['termunit'], item['repaymentmethod'],item['startdate'],item['enddate'])

        sql = 'insert into newbid_product_info_table(platformid,producttype,productname,producturl,' \
              'productid,amount,balance,maxrate,minrate,term,termunit,repaymentmethod,startdate,enddate) ' \
              'values( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self._cur = self._conn.cursor()
            self._cur.execute(sql,params=values)
            self.commit_trans()
            self._cur.close()

            print '4-新标数据保存完毕'.encode('utf-8')

        except Exception,e:
            self._conn.rollback()
            print "5-新标数据保存失败，失败信息为： %s" % e

    # 新标数据更新
    # @balance:新的余额值
    # @platformid:平台id
    # @productid:产品id
    def update(self, balance, platformid, productid):
        pars = (balance, platformid, productid)
        sql = 'update newbid_product_info_table SET balance=%s where platformid=%s and productid=%s'
        try:
            self._cur = self._conn.cursor()
            self._cur.execute(sql,params=pars)
            self.commit_trans()
            self._cur.close()

            print '6-新标数据更新完毕'.encode('utf-8')

        except Exception,e:
            self._conn.rollback()
            print "7-新标数据更新失败，出错信息为： %s" % e

