# -*- coding: utf-8 -*-
import cx_Oracle
import sys
import pandas as pnd

reload(sys)
sys.setdefaultencoding('utf-8')


##alex modi
def orcltest():
    try:
        conn = cx_Oracle.connect("c##hxdata/Abcd1234@orcl213")
        sqlstr='select  code, name from stkdata1 where rownum<10'
        #sqlstr=u'select  代码 as code,名称 as , name from stkdata1 where rownum<10'
        results = pnd.read_sql(sqlstr, conn)
        print results[1]
        results.to_csv('3.csv')
        conn.close
    except Exception, e:
        print "oracle  Error %s" % (e.args[0])


if __name__ == '__main__':
    print u'Oracle 连接测试中....'
    orcltest()
