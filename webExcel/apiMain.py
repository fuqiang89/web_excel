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
from moudle.Mysql_orm import table_operate
from moudle.table_orm import table_orm
from moudle.operate_register import operate_register
from config import dataPath
tl=template.Loader(os.path.join(TP, "webExcel/srv_html"))
table_operate=table_operate()
table_orm=table_orm()
operate_register=operate_register()
##namp
from moudle.nmapApi import Snmap
###

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
                self.write(json_encode(dhistory))
            except Exception:
                self.render("page_500.html")

##################################
#################nmap#####################
        if i.stype == "nmap":
            if i.slevel == "xProfile":
                try:
                    nmap=table_operate.getSelf("""SELECT * from table_nmap
                    WHERE srv_num =
                    (SELECT srv_num from s_table WHERE id = {0:s})
                    order by id desc limit 1""".format(i.id))
                    for dkey in nmap:
                        dkey['opTime']=str(dkey['opTime'])
                    self.write(json_encode(nmap))
                except Exception,e:
                    print(e)
                    self.render("page_500.html")
            if  i.slevel == "scan":
                try:
                    id=i.id
                    srv_num=table_operate.getSelf("""SELECT srv_num from s_table
                     where id={0:s}""".format(id))[0]['srv_num']

                    nmapdata=Snmap().nmap_port_sev(srv_num)
                    if nmapdata['status'] == True:
                        nmapdata['data']['reslut']='ok'
                        self.write(json_encode(nmapdata))
                    else:
                        nmapdata['reslut']='failure'
                        self.write(json_encode(nmapdata))
                except Exception,e:
                    print(e)


##################################