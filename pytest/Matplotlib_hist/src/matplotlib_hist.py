# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import mysql.connector as sql
import pandas as pnd


def hist1():
    mu, sigma = 100, 15
    x = mu + sigma * np.random.randn(10000)
    n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

    # print patches
    y = mlab.normpdf(bins, mu, sigma)
    l = plt.plot(bins, y, 'r--', linewidth=1)

    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    plt.axis([40, 160, 0, 0.03])
    plt.grid(True)
    plt.show()


def hist2():
    x = np.random.randn(1000000)
    plt.hist(x, 100)
    plt.title(r'Normal distribution with $\mu=0,\sigma=1$')
    # plt.savefig('matplotlib_histogram.png')
    plt.show()


def hist3():
    try:
        conn = sql.connect(host='192.168.1.212', user='root', passwd='abc123,./', db='wxt', port=3306, charset='utf8')
        cur = conn.cursor()
        cur.execute('select  from product where producttype=5')
        results = cur.fetchall()

        ##取出第二列
        amounts = [x[2] for x in results]
        plt.hist(amounts, 100)
        plt.show()
    except Exception, e:
        print "Mysql Error %s" % (e.args[0])


def hist4():
    try:
        conn = sql.connect(host='192.168.1.212', user='root', passwd='abc123,./', db='test', port=3306, charset='utf8')
        results = pnd.read_sql('select * from test_analysis1 limit 0 ,1000', conn)
        plt.hist(results['pid'], 100)
        plt.show()
    except Exception, e:
        print "Mysql Error %s" % (e.args[0])


def main():
    # hist1()
    # hist2()
    hist4()


if __name__ == '__main__':
    main()
