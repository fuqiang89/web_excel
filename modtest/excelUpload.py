__author__ = 'fuqiang'
import xlrd
import torndb
import sys
#from moudle.nmapPy import sdb
from config import *
myDb=str(12306)
class mysqlConn():
    def __init__(self):
        self.mysqld = torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)
    def mysqld(self):
        mysqld=self.mysqld
        return mysqld
    def __del__(self):
        self.mysqld.close()
sdb=mysqlConn().mysqld
book = xlrd.open_workbook("ph.xlsx")
sheet = book.sheet_by_name("12")


for r in range(1, sheet.nrows):
    try:
        mail= sheet.cell(r,12).value
        mail=str(mail).strip()
        #print(mail)

        data=sdb.get("""select * from user where phone='%s'""" % mail)
        if data:
            print(data)
    except Exception, exc:
        print(sys.exc_info())
        #print mail