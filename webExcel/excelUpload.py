__author__ = 'fuqiang'
import xlrd
import torndb
import sys
from moudle.nmapPy import sdb
book = xlrd.open_workbook("xx.xls")
sheet = book.sheet_by_name("x1")


print sheet.nrows
for r in range(1, sheet.nrows):
    try:
        updict={}
        updict['Srv_used'] = sheet.cell(r,0).value.replace('}','}/n')

        updict['srv_num']  = 'srv_' + sheet.cell(r,1).value

        updict['inter_ip'] = sheet.cell(r,2).value.replace('\n','/n')

        updict['local_ip'] = sheet.cell(r,3).value.replace('\n','/n')
        updict['rank_one'] = sheet.cell(r,4).value


        updict['admin'] = sheet.cell(r,5).value



        sdb.insert_by_dict('s_table',updict)
        print(updict)
    except Exception, exc:
        print(sys.exc_info())
        print r
        exit()