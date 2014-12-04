# -*- coding: utf-8 -*-
__author__ = ''
from config import *
import torndb
from Storage import storage
from table_orm import table_orm
table_orm=table_orm()
def GC_set(obj):
    return ""
class table_operate:
    def __init__(self):
        self.sdb=torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)
    def __del__(self):
        self.sdb.close()
    def getAll(self):
        items=self.sdb.query("select * from s_table  order by id desc")
        return items
    #def search(self,keys):
    #    sql="""select * FROM s_table WHERE srv_num REGEXP '%s' OR inter_ip REGEXP '%s' \
    #     OR local_ip REGEXP '%s' OR role REGEXP '%s' OR admin REGEXP '%s' OR re_man REGEXP '%s'"""
    #    items=sdb.query(sql % (keys,keys,keys,keys,keys,keys))
    #    return items

#自定义查询
    def getSelf(self,Sql):
        items=self.sdb.query(Sql)
        return items

    def delEntityById(self,id):
        return self.sdb.execute("""delete from s_table where id=%s""",id)


    def getEntityById(self,id):
        if id:
            id=int(id)
            item=self.sdb.get("""select * from s_table where id=%s""",id)
            return item
        else:
            return None

    def getEntityBySrv_num(self,srv_num):
        if srv_num:
            item=self.sdb.get("""select * from s_table where srv_num=%s""",srv_num)
            return item
        else:
            return None



    def getId(self,id):
        if id:
            id=int(id)
            item=self.sdb.get("""select * from s_table where id=%s""",id)
            redata=table_orm.replace(item,type='html')
            return storage(redata)
        else:
            return None
    def getRowsBySqlwhere(self,sqlwhere):
        items=self.sdb.query("""select * from s_table where id>0 """+sqlwhere)
        if items:
            for i in items:
                i=storage(i)
        return items

    def update(self,obj):
        obj=storage(obj)
        if obj.id > 0:
            where='id=%s' % obj.id
            del obj["id"]
            return self.sdb.update_by_dict('s_table',obj,where)
        else:
            return "ERROR xxxx!!"
    def insert(self,obj):
        obj=storage(obj)
        if obj.id:
            #print(obj.id)
            return "ERROR xxxx!!"
        else:
            del obj["id"]
            return self.sdb.insert_by_dict("s_table",obj)

    def getRowBySqlwhere(self,sqlwhere):
        item=self.sdb.get("""select * from s_table where id>0 """+sqlwhere)
        if item:
            item=storage(item)
        return item