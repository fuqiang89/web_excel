# -*- coding: utf-8 -*-

import torndb

myHost='10.0.0.110'
myPort='3306'
myDb='srv_table_test'
myUser='root'
myPasswd='123456'

TP="G:\\BaiduYunDownload\\webExcel\\web_excel\\"
dataPath="G:\\BaiduYunDownload\\webExcel\\web_excel\\data\\"
class mysqlConn():
    def __init__(self):
        self.mysqld = torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)
    def mysqld(self):
        mysqld=self.mysqld
        return mysqld
    def __del__(self):
        self.mysqld.close()


#sdb=mysqlConn().mysqld









