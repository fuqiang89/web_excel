# -*- coding: utf-8 -*-

import torndb

myHost='172.16.10.101'
myPort='3306'
myDb='srv_table'
myUser='srv_table_user'
myPasswd='srv_table_fuqiang123'

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









