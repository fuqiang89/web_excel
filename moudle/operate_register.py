__author__ = 'fuqiang'
from config import *
from moudle.table_orm import table_orm
import datetime

class operate_register():
    def __init__(self):
        self.sdb=torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)
    def __del__(self):
        self.sdb.close()
    def reg_del(self,id,table_name,fields,opName,xExplain):
        fields=', '.join(fields)
        tmptime=datetime.datetime.now()
        #print(opName)
        sql_all="""select %s from %s where id = %s""" % (fields,table_name,id)
        item=self.sdb.get(sql_all)
        item['act']='del'
        item['op_time']=tmptime
        item['opName']= opName
        item['table_name']=table_name
        item['xExplain']=xExplain
        #print(item)
        self.sdb.insert_by_dict('table_op_reg',item)
    def reg_add_update(self,obj,table_name,act,opName,xExplain):
        tmptime=datetime.datetime.now()
        #print(obj,table_name,act,opName,xExplain)
        obj['table_name']=table_name
        obj['op_time']=tmptime
        obj['opName']=opName
        obj['act']=act
        obj['xExplain']=xExplain
        if act=='add':
            autoid=self.sdb.get("select max(id) as id from %s" % (table_name))['id']
            obj['id']=autoid
        self.sdb.insert_by_dict("table_op_reg",obj)

if __name__=='__main__':
    table_orm=table_orm()
    op=operate_register()
    fields=table_orm.get_fields("srv_table")['fields']
    op.reg_del('79','s_table',fields)
