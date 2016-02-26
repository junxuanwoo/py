# coding=utf-8
import pymssql
import pandas as pnd
import matplotlib.pyplot as plt
import MySQLdb


def getconn():
    return pymssql.connect(host='192.168.1.212', user='sa', password='abc123,./', database='wxtdata', charset="utf8")


def piddist():
    sqlstr = 'select amount as pid from itemdata1'
    conn = getconn()
    results = pnd.read_sql(sqlstr, conn)
    plt.hist(results['pid'], 100)
    plt.show()


def caphold():
    sqlstr = 'select datadate,sum(amount) as amount from itemdays group by datadate order by datadate'
    conn = getconn()
    results = pnd.read_sql(sqlstr, conn)
    # plt.plot_date(results['datadate'],results['amount'],'-')
    plt.plot(results['datadate'], results['amount'], '-')
    plt.show()

def nowhold():
    #sqlstr="select webid,sum(nowdaymoneys) as ndms from t_bi_holdcap where cdate='2015-12-11' group by webid order by 2"
    #sqlstr="select webid,sum(investmoney) as ndms from t_bi_holdcap where cdate='2015-12-11' group by webid order by 1"
    sqlstr="select webid,sum(investmoney) as ndms from t_bi_holdcap where cdate='2015-12-11' group by webid order by 1"
    conn=MySQLdb.connect(host='192.168.1.212', user='root', passwd='abc123,./', db='test', port=3306, charset='utf8')
    results = pnd.read_sql(sqlstr, conn)
    #plt.plot(results['webid'], results['ndms'], '-')
    plt.bar(results['webid'], results['ndms'])
    #plt.pie(results['ndms'])
    plt.show()

def main():
    # piddist()
    nowhold()


if __name__ == '__main__':
    main()
