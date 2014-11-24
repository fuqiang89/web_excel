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
    def replace(self,item,type=None):
        if type == 'html':
            for value in item:
                if value in ['Srv_used','local_ip','inter_ip']:
                    item[value]= "\n".join(item[value].split("<br>"))
                    print item[value]
        else:
            for value in item:
                if (item[value], basestring):
                    item[value]=(item[value]).replace('\n','<br>')
        return item
#if __name__ == "__main__":
#    t=table_orm()
