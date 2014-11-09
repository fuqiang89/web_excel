# -*- coding: utf-8 -*-
__author__ = ''
from config import sdb
from Storage import storage
from table_orm import table_orm
table_orm=table_orm()
def GC_set(obj):
    return ""
class table_operate:

    #fields=table_orm.get_fields_array("srv_table_fileds")

    def getAll(self):
        items=sdb.query("select * from s_table  order by id desc")
        return items
    #def search(self,keys):
    #    sql="""select * FROM s_table WHERE srv_num REGEXP '%s' OR inter_ip REGEXP '%s' \
    #     OR local_ip REGEXP '%s' OR role REGEXP '%s' OR admin REGEXP '%s' OR re_man REGEXP '%s'"""
    #    items=sdb.query(sql % (keys,keys,keys,keys,keys,keys))
    #    return items


    def delEntityById(self,id):
        return sdb.execute("""delete from s_table where id=%s""",id)
    def getEntityById(self,id):
        if id:
            id=int(id)
            item=sdb.get("""select * from s_table where id=%s""",id)
            return storage(item)
        else:
            return None
    def getRowsBySqlwhere(self,sqlwhere):
        items=sdb.query("""select * from s_table where id>0 """+sqlwhere)
        if items:
            for i in items:
                i=storage(i)
        return items
    def update(self,obj):
        obj=storage(obj)
        if obj.id > 0:
            where='id=%s' % obj.id
            del obj["id"]
            return sdb.update_by_dict('s_table',obj,where)
        else:
            return "ERROR xxxx!!"
    def insert(self,obj):
        obj=storage(obj)
        if obj.id:
            #print(obj.id)
            return "ERROR xxxx!!"
        else:
            del obj["id"]
            return sdb.insert_by_dict("s_table",obj)
    def getRowBySqlwhere(self,sqlwhere):
        item=sdb.get("""select * from s_table where id>0 """+sqlwhere)
        if item:
            item=storage(item)
        return item