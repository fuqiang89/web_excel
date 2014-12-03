__author__ = 'fuqiang'
from config import *
from moudle.table_orm import table_orm
import datetime

class operate_register():
    def __init__(self):
        self.sdb=torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)
    def __del__(self):
        self.sdb.close()
    def reg_del(self,id,table_name,fields):
        fields=', '.join(fields)
        tmptime=datetime.datetime.now()
        sql_all="""select %s from %s where id = %s""" % (fields,table_name,id)
        item=self.sdb.get(sql_all)
        item['act']='del'
        item['op_time']=tmptime
        item['table_name']=table_name
        self.sdb.insert_by_dict('table_op_reg',item)
    def reg_add(self,obj,table_name,act):
        tmptime=datetime.datetime.now()
        obj['table_name']=table_name
        obj['op_time']=tmptime
        obj['act']=act
        if act=='add':
            obj['id']=0
        self.sdb.insert_by_dict("table_op_reg",obj)

if __name__=='__main__':
    table_orm=table_orm()
    op=operate_register()
    fields=table_orm.get_fields("srv_table")['fields']
    op.reg_del('79','s_table',fields)
