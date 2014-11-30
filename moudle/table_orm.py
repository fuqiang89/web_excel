# -*- coding: utf-8 -*-
__author__ = 'fuqiang'
from config import sdb
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
class  table_orm():
    def get_fields(self,table_name):
        item=sdb.get("""select fields from table_module where table_name = '%s' """ % table_name)
        item['fields']=item['fields'].split(',')
        return item
    def get_useAdmin(self,table_name):
        item=sdb.get("""select useAdmin from table_module where table_name = '%s' """ % table_name)
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
                        print(item[value])
                        item[value]=item[value].replace('\n',r'/n')
                        print(item[value])

        return item


#if __name__ == "__main__":
#    t=table_orm()
