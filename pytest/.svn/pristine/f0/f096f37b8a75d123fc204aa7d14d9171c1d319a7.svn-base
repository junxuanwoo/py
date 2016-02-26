# -*- coding: utf-8 -*-
import pymssql

conn = pymssql.connect(host='192.168.88.109', user='sa', password='Abcd1234', database='wxtdata')

mlist = conn.cursor()
msql = 'select * FROM gl'
mlist.execute(msql)
for (gl,i, p) in mlist.fetchall():
    print str(gl) + "\t" + str(p)
conn.close()
