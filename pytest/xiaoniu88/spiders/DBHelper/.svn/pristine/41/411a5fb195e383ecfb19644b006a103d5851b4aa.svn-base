#coding:UTF-8
import threading
import mysql.connector
import sys
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')


class DBConn: #单例类，只实例化一次
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
                                        db='product_info',
                                        port=3306,
                                        charset='utf8')

    def __del__(self):
        self._conn.close()

    @staticmethod
    def get_instance(): #静态方法
        if DBConn._instance is None:
            DBConn.mutex.acquire()
            if DBConn._instance is None:
                print "1-数据连接组件已创建".encode('utf-8')
                DBConn._instance = DBConn()
            else:
                print "2-无法创建数据连接组件的多个实例".encode('utf-8')
            DBConn.mutex.release()
        return DBConn._instance

    def commit_trans(self): # 提交事务并关闭游标
        self._conn.commit()
        self._cur.close()

    #获取最大的产品ID，如果没有产品则返回0
    def get_last_id(self):
        sql = 'select IFNULL(max(prdid),0) maxid from ppmoney_products_list ;'
        try:
            self._cur = self._conn.cursor()
            self._cur.execute(sql)
            r = self._cur.fetchone()
            self._cur.close()
            print '3-小牛在线最大的产品ID获取完毕'.encode('utf-8')
            return int(r[0])+1
        except Exception, e:
            print "Mysql Error %s" % e

    def save_url(self,parURL):
        sql = "insert into t_url_tmp(purl,ptype) select %s,%s"
        try:
            self._cur = self._conn.cursor()
            self._cur.executemany(sql,parURL)
            self.commit_trans()
            print '4-1-小牛在线产品数据保存完毕'.encode('utf-8')
        except Exception,e:
            self._conn.rollback()
            print "5-1-小牛在线产品数据保存失败，出错信息为： %s" % e