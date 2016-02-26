# -*- coding: utf-8 -*-
import MySQLdb
import cx_Oracle
import mysql.connector
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


##alex modi
def orcltest():
    try:
        conn = cx_Oracle.connect("c##hxdata/Abcd1234@orcl213")
        print u'建立ORACLE连接正常'

        cur = conn.cursor()

        print u'建立ORACLE游标正常'
        r = cur.execute("select * from stkdata where rownum<10")

        print u'查询语句正常，返回第一条记录'
        print r.fetchone()  # 乱码

        print u'返回前10条记录正常'
        for tmp in r:
            print tmp[1], tmp[0]  # 不乱吗

        r.close
        conn.close
        print u'ORACLE连接关闭'
    except Exception, e:
        print "oracle  Error %s" % (e.args[0])


def mysqltest1():
    try:
        conn = mysql.connector.connect(
            host='192.168.1.212', user='root', passwd='abc123,./', db='wxt', port=3306, charset='utf8')
        print u'mysql.connector建立mysql连接正常'
        cur = conn.cursor()
        print u'建立mysql游标正常'

        cur.execute(
            'select account,username from member where username  is not null')

        print u'查询语句正常，返回游标'

        result = cur.fetchone()
        print result

        results = cur.fetchmany(10)
        for r in results:
            print r
        print u'返回前10条记录正常'

        results = cur.fetchall()
        for r in results:
            print r[0], r[1]

        # conn.commit()
        cur.close()
        conn.close()
        print u'Mysql连接关闭'
    except Exception, e:
        print "Mysql Error %s" % (e.args[0])


def mysqltest2():
    try:
        # conn = mysql.connector.connect(
        conn = MySQLdb.connect(
            host='192.168.1.212', user='root', passwd='abc123,./', db='wxt', port=3306, charset='utf8')
        print u'MySQLdb建立mysql连接正常'
        cur = conn.cursor()
        print u'建立mysql游标正常'

        cur.execute(
            'select account,username from member where username  is not null')

        print u'查询语句正常，返回游标'

        result = cur.fetchone()
        print result

        results = cur.fetchmany(10)
        for r in results:
            print r
        print u'返回前10条记录正常'

        results = cur.fetchall()
        for r in results:
            print r[0], r[1]

        # conn.commit()
        cur.close()
        conn.close()
        print u'Mysql连接关闭'
    except Exception, e:
        print "Mysql Error %s" % (e.args[0])


def main():
    print u'mysql.connector 连接测试中....'
    mysqltest1()

    print u'MySQLdb 连接测试中....'
    mysqltest2()

    print u'Oracle 连接测试中....'
    orcltest()

    # 双击打开暂停窗口用
    # raw_input()


if __name__ == '__main__':
    main()
