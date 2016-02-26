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
        sql = 'select IFNULL(max(prdid),0) maxid from product_info.gscf_products_list ;'
        try:
            self._cur = self._conn.cursor()
            self._cur.execute(sql)
            r = self._cur.fetchone()
            self._cur.close()
            print '3-果树财富最大的产品ID获取完毕'.encode('utf-8')
            return r[0]
        except Exception, e:
            print "Mysql Error %s" % e

    def save_all_info_to_db(self,parPrdInfo,parBorrowerInfo,parBorrowerAuthInfo,parUserJoinLogs):
        sqlSavePrdInfo = self.genSavePrdInfoSQL()
        sqlSaveBorrowerInfo = self.genSaveBorrowerInfoSQL()
        sqlSaveBorrowerAuthInfo = self.genSaveBorrowerAuthInfoSQL()
        sqlSaveUserJoinLogs = self.genSaveUserJoinLogsSQL()
        try:
            self._cur = self._conn.cursor()
            self._cur.execute(sqlSavePrdInfo,params=self.getPrdInfoArgs(parPrdInfo))
            self._cur.execute(sqlSaveBorrowerInfo,params=self.getBorrowerInfoArgs(parBorrowerInfo))
            self._cur.execute(sqlSaveBorrowerAuthInfo,params=self.getBorrowerAuthInfArgs(parBorrowerAuthInfo))
            self._cur.executemany(sqlSaveUserJoinLogs,params=self.chgUserJoinLogsFormat(parUserJoinLogs))
            self.commit_trans()
            print '4-果树财富数据保存完毕'.encode('utf-8')
        except Exception,e:
            self._conn.rollback()
            print "5-果树财富数据保存失败，出错信息为： %s" % e

    def genSavePrdInfoSQL(self):
        sql = "insert into product_info.gscf_products_list(cretime,prdid,pfno,prdname,hasmortgage,borrower,\
               borrowamount,borrowamountunit,borrowrate,borrowrateunit,borrowduelimit,borrowduelimitunit,\
               publishtime,maxinvestamount,repaymenttype,expected,borrowtype) \
               select sysdate(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"
        return sql

    def getPrdInfoArgs(self,prdInfo):
        args=[prdInfo.prdid,prdInfo.pfno,prdInfo.prdname,prdInfo.hasmortgage,prdInfo.borrower,prdInfo.borrowamount,
              prdInfo.borrowamountunit,prdInfo.borrowrate,prdInfo.borrowrateunit,prdInfo.borrowduelimit,
              prdInfo.borrowduelimitunit,prdInfo.publishtime,prdInfo.maxinvestamount,prdInfo.repaymenttype,
              prdInfo.expected,prdInfo.borrowtype]
        return args

    def genSaveBorrowerInfoSQL(self):
        sql = "insert into product_info.gscf_borrower_info(cretime,pfno,borrowerid,sex,age,education,marry,incomerange,\
               housing,hascar,industry,unpaid,sumborrowamount,successcount,repaymentcount,overduecount) select  \
               sysdate(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"
        return sql

    def getSaveBorrowerInfoArgs(self,borrowerInfo):
        args=[borrowerInfo.pfno,borrowerInfo.borrowerid,borrowerInfo.sex,borrowerInfo.age,borrowerInfo.education,
              borrowerInfo.marry,borrowerInfo.incomerange,borrowerInfo.housing,borrowerInfo.hascar,
              borrowerInfo.industry,borrowerInfo.unpaid,borrowerInfo.sumborrowamount,
              borrowerInfo.successcount,borrowerInfo.repaymentcount,borrowerInfo.overduecount]
        return args

    def genSaveBorrowerAuthInfoSQL(self):
        sql = "insert into product_info.gscf_borrower_auth_info(pfno,borrowerid,authhascar,authhascartime,\
               authother,authothertime,authid,authidtime,authmortgage,authmortgagetime,authdomicile,\
               authdomiciletime,autoworked,autoworkedtime) select sysdate(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
               %s,%s,%s,%s"
        return sql

    def getSaveBorrowerAuthInfoArgs(self,borrowerAuthInfo):
        args=[borrowerAuthInfo.pfno,borrowerAuthInfo.borrowerid,borrowerAuthInfo.sex,borrowerAuthInfo.age,
              borrowerAuthInfo.education,borrowerAuthInfo.marry,borrowerAuthInfo.incomerange,borrowerAuthInfo.housing,
              borrowerAuthInfo.hascar,borrowerAuthInfo.industry,borrowerAuthInfo.unpaid,borrowerAuthInfo.sumborrowamount,
              borrowerAuthInfo.successcount,borrowerAuthInfo.repaymentcount,borrowerAuthInfo.overduecount]
        return args

    def genSaveUserJoinLogsSQL(self):
        sql = "insert into product_info.gscf_users_join_logs(cretime,pfno,prdid,investseq,investuser,investamount,\
               investtime,investstatus) select sysdate(),%s,%s,%s,%s,%s,%s,%s"
        return sql

    #把 UserJoinLogs 集合转换为参数格式
    def chgUserJoinLogsFormat(self,parUserJoinLogs):
        join_list=[]
        for userJoinLog in parUserJoinLogs:
            join_rec = (userJoinLog.pfno,userJoinLog.prdid,userJoinLog.investseq,userJoinLog.investuser,
                        userJoinLog.investamount,userJoinLog.investtime,userJoinLog.investstatus)
            join_list.append(join_rec)
        return join_list












