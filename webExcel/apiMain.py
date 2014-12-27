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
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
#################
from config import TP
from moudle.Mysql_orm import table_operate
from moudle.table_orm import table_orm
from moudle.operate_register import operate_register
from moudle.accountMod import *
#################

tl=template.Loader(os.path.join(TP, "webExcel/srv_html"))
table_operate=table_operate()
table_orm=table_orm()
operate_register=operate_register()
auth=Authentication()
##namp
from moudle.nmapApi import Snmap
###

class  API(basehandler):
    executor = ThreadPoolExecutor(2)
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        i=self.input()
        i.username=self.current_user


#############xProfile##############
        if i.stype == "xProfile":
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
                    args=''
                    nmapdata = yield self.nmapScan(srv_num,args)
                    self.write(json_encode(nmapdata))
                    self.finish()
                except Exception,e:
                    print(e)
                try:
                    nip=i.nip
                    args=i.args
                    nmapdata = yield self.nmapScan(nip,args)
                    self.write(json_encode(nmapdata))
                    self.finish()
                except Exception,e:
                    print(e)


    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        i=self.input()
        i.username=self.current_user
        if i.stype == "changePasswd":
            try:
                reslut_cPw=auth.change_passwd(i.username,i.old_passwd,i.new_passwd)
                if reslut_cPw == True:
                    self.clear_cookie("user")
                    self.write("ok")
            except Exception,e:
                print(e)

##########nmap#########
    @run_on_executor
    def nmapScan(self,obj,args):
        if not args:
            args=' -T4  -sUT   -n '
        return Snmap().nmap_port_sev(obj,arguments=args)
##################################