__author__ = 'fuqiang'
import xlrd
import torndb
import sys
from config import sdb
book = xlrd.open_workbook("t1.xlsx")
sheet = book.sheet_by_name("test")


print sheet.nrows
for r in range(1, sheet.nrows):
    try:
        updict={}
        updict['srv_num']  = sheet.cell(r,0).value
        updict['inter_ip'] = sheet.cell(r,1).value.replace('\n','\\n')
        updict['local_ip'] = sheet.cell(r,2).value.replace('\n','\\n')
        updict['rank_one'] = sheet.cell(r,3).value
        updict['Srv_used'] = sheet.cell(r,4).value.replace('}','}\\n')
        updict['re_admin'] = sheet.cell(r,5).value
        updict['admin'] = sheet.cell(r,6).value
        updict['note']  = sheet.cell(r,7).value
        sdb.insert_by_dict('s_table',updict)
    except Exception, exc:
        print(sys.exc_info())
        print r
