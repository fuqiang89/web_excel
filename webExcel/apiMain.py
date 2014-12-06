# -*- coding: utf-8 -*-
__author__ = 'fuqiang'
import os,sys
import json
# from bson import json_util
from tornado import template
from tornado.web import RequestHandler
import tornado.web
from Storage import storage
from utils import *
from tornado.escape import json_encode
from basehandler import basehandler
from config import TP
from moudle.srv_m import table_operate
from moudle.table_orm import table_orm
from moudle.operate_register import operate_register
from config import dataPath
tl=template.Loader(os.path.join(TP, "webExcel/srv_html"))
table_operate=table_operate()
table_orm=table_orm()
operate_register=operate_register()
#url/api?stype=xx&
class  API(basehandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        i=self.input()
        i.username=self.current_user


#############xProfile##############
        if i.stype == "xProfile":
            # fields=table_orm.get_fields("srv_table")['fields']
            #i.recs=InitStorage(i,fields)
            i.recs=table_operate.getEntityById(i.id)
            self.write(json_encode(i))
######## End   xProfile ##########
##########history##################
        if i.stype == "history":
            try:
                dhistory=table_operate.getSelf("select * from table_op_reg order by autoid desc " )
                for dkey in dhistory:
                    dkey['op_time']=str(dkey['op_time'])

            except Exception:
                self.render("page_500.html")
            self.write(json_encode(dhistory))
##################################
#################nmap#####################
        if i.stype == "nmap":
            try:
                dnmap=table_operate.getSelf("SELECT * from table_nmap WHERE srv_num = (SELECT srv_num from s_table WHERE id = %s)" % i.id )
                for dkey in dnmap:
                    dkey['opTime']=str(dkey['opTime'])
            except Exception,e:
                self.render("page_500.html")
            self.write(json_encode(dnmap))
##################################