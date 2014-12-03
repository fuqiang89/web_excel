# -*- coding: utf-8 -*-
__author__ = 'fuqiang'
from config import *
import torndb
import tablib
import sys,time
reload(sys)
sys.setdefaultencoding( "utf-8" )

class  table_orm():
    def __init__(self):
        self.sdb=torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)
    def __del__(self):
        self.sdb.close()
    def get_fields(self,table_name):
        item=self.sdb.get("""select fields from table_module where table_name = '%s' """ % table_name)
        item['fields']=item['fields'].split(',')
        return item
    def get_useAdmin(self,table_name):
        item=self.sdb.get("""select useAdmin from table_module where table_name = '%s' """ % table_name)
        item['useAdmin']=item['useAdmin'].split(',')
        return item
    def replace(self,item,fields,type=None):
        if type == 'out':
            for value in item:
                if value in fields:
                    if item[value]:
                        item[value]= item[value].replace('\\n','<br>').replace('\n','<br>')
        if type == 'in':
            for value in item:
                if value in fields:
                    if item[value]:
                        item[value]=item[value].replace('\n',r'/n')
        return item

    def exportExecl_json(self,fields,dataJson):
        try:
            data=[]
            fields.append('state')
            headers = tuple(fields)
            data = tablib.Dataset(*data, headers=headers)
            dataJson=dataJson.replace('<br>','\\r')
            data.json=dataJson
            filename="xTable_%s.xlsx" % (time.time())
            f=open('%s%s' % (dataPath,filename),'wb')
            f.write(data.xlsx)
            f.close()
            return filename
        except Exception,exc:
            print(sys.exc_info())
            print(exc)
            return "False"


if __name__ == "__main__":
    t=table_orm()
    dataJson='[{"first_name": "John","last_name": "123"},{"first_name": "222","last_name": "hhh"}]'
    print  t.exportExecl_json(dataJson)