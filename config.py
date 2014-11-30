# -*- coding: utf-8 -*-

import torndb

myHost='192.168.182.129'
myPort='3306'
myDb='demo'
myUser='root'
myPasswd='123456'

TP="G:\\BaiduYunDownload\\webExcel\\web_excel\\"

class mysqlConn():
    def __init__(self):
        self.mysqld = torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)
    def mysqld(self):
        mysqld=self.mysqld
        return mysqld
    def __del__(self):
        self.mysqld.close()


sdb=mysqlConn().mysqld









