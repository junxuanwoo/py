#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created on 2011-2-19
# @author: xiaoxiao
import MySQLdb
import sys
#__all__ = ['MySQL']
class MySQL():
    '''
    MySQL
    '''
    conn = ''
    cursor = ''
    def __init__(self,host='localhost',user='root',passwd='root',db='mysql',charset='utf8'):

        """MySQL Database initialization """
        try:
            self.conn = MySQLdb.connect(host='192.168.0.212',user='root',passwd='abc123,./',db='mysql')
        except MySQLdb.Error,e:
            errormsg = '连接失败\nERROR (%s): %s' %(e.args[0],e.args[1])
            print errormsg
            sys.exit()

        self.cursor = self.conn.cursor()

    def query(self,sql):
        """  Execute SQL statement """
        return self.cursor.execute(sql)

    def show(self):
        """ Return the results after executing SQL statement """
        return self.cursor.fetchall()

    def __del__(self):
        """ Terminate the connection """
        self.conn.close()
        self.cursor.close()

#test
# if __name__ == '__main__':
#
#     mysql = MySQL()
#     mysql.query('select * from user')
#     result = mysql.show()
#     print len(result)
#     print result[1]