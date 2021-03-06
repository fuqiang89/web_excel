# -*- coding: utf-8 -*-
__author__ = ''
from config import *
import torndb
from Storage import storage
from tableOrm import table_orm
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
##search

    #def search(self,keys):
    #    sql="""select * FROM s_table WHERE srv_num REGEXP '%s' OR inter_ip REGEXP '%s' \
    #     OR local_ip REGEXP '%s' OR role REGEXP '%s' OR admin REGEXP '%s' OR re_man REGEXP '%s'"""
    #    items=sdb.query(sql % (keys,keys,keys,keys,keys,keys))
    #    return items

    def _sql_where_search(self,_search,Fileds,Filter,tablename,ord='OR'):
        sql='select * FROM {0:s} WHERE '.format(tablename)
        for i in Fileds:
            sql=sql + " {0:s} {1:s} '{2:s}' {3:s} ".format(i,Filter,_search,ord)
        sql=sql[:-3]
        return sql

    def search(self,_search,Fileds,Filter,tablename):
        if Filter in ['REGEXP','LIKE']:
            sql=self._sql_where_search(_search,Fileds,Filter,tablename,ord='OR')
            #print(sql)
            items=self.sdb.query(sql)
            return items
        if Filter == 'NOT_REGEXP':
            Filter='NOT REGEXP'
            sql=self._sql_where_search(_search,Fileds,Filter,tablename,ord='OR')
            items=self.sdb.query(sql)
            return items




#自定义查询
    def getSelf(self,Sql):
        items=self.sdb.query(Sql)
        return items
    def getone(self,Sql):
        items=self.sdb.get(Sql)
        return items
    def mdb(self):
        return self.sdb
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
            try:
                self.sdb.update_by_dict('s_table',obj,where)
                return True
            except Exception,e:
                return e
        else:
            return "更新错误！id={0}".format(obj.id)
    def insert(self,obj):
        obj=storage(obj)
        if obj.id:
            return "add error !!"
        else:
            del obj["id"]
            try:
                self.sdb.insert_by_dict("s_table",obj)
                return True
            except Exception,e:
                return e

    def getRowBySqlwhere(self,sqlwhere):
        item=self.sdb.get("""select * from s_table where id>0 """+sqlwhere)
        if item:
            item=storage(item)
        return item
    ##insert by dict
    def insert_by_dict(self,table_name,dict):
        return self.sdb.insert_by_dict(table_name,dict)

if __name__ == '__main__':
    tt=table_operate()
    with open('port.txt') as f:
        a=1
        for ip in f:
            a=a+1
            print(a)
            ip=str(ip.replace(' ','').replace('\n',''))
            dd=tt.search(ip,['srv_num','inter_ip','local_ip'],'REGEXP','s_table')
            if dd:
                print(dd)