# -*- coding: utf-8 -*-
__author__ = 'fuqiang'
from config import sdb
class  table_orm():
    def get_fields(self,table_name):
        item=sdb.get("""select fields from table_module where table_name = '%s' """ % table_name)
        item['fields']=item['fields'].split(',')
        return item
    def get_useAdmin(self,table_name):
        item=sdb.get("""select useAdmin from table_module where table_name = '%s' """ % table_name)
        item['useAdmin']=item['useAdmin'].split(',')
        return item
#if __name__ == "__main__":
#    t=table_orm()
