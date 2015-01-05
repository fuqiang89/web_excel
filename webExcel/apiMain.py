# -*- coding: utf-8 -*-
__author__ = 'fuqiang'
import os,sys
import json,ast
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
                    nmap[0]['opTime']=str(nmap[0]['opTime'])
                    nmapdata=nmap[0]['nmapdata'][1:-1]
                    port_ignore=[25,110,111]
                    port_state=['filtered','closed','open|filtered']
                    nmapdata=ast.literal_eval(nmapdata)
                    renmapdata=[]
                    for portinfo in nmapdata:

                        if (portinfo['nport'] in port_ignore) \
                            or (portinfo['state'] in port_state):
                            print(portinfo['nport'],portinfo['state'])
                        else:
                            print(portinfo['nport'],portinfo['state'])
                            renmapdata.append(portinfo)
                    nmap[0]['nmapdata']=renmapdata
                    #print(nmap)
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
#######################
        if  "myProfile" in i.values():
            self.render('user/account_info.html',i=i)

################

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        i=self.input()

        i.username=self.current_user
        keys=['stype','slevel']

        ckeck_keys=set(i.keys()).intersection(set(keys))
        if  len(list(ckeck_keys))!=2:
            print(len(list(ckeck_keys)))
            self.clear()
            self.set_status(500)
            self.finish(json_encode({"success": False}))
            return False



        if  i.stype == 'account':
            if i.slevel == 'firstChangePasswd':
                try:
                    reslut_cPw=auth.change_passwd(i.username,i.old_passwd,i.new_passwd)
                    if reslut_cPw == True:
                        self.clear_cookie("user")
                        self.write("ok")
                        return True
                except Exception,e:
                    print(e)
            if i.slevel == 'changeUsername':
                try:
                    print(i.value)
                    reslut_cUn=auth.change_username(i.username,i.value)
                    if reslut_cUn:
                        self.clear_cookie("user")
                        self.finish(json_encode({"success": True}))
                        return True
                    else:
                        self.write(json_encode({"success": False}))
                        return False
                except Exception,e:
                    print(e)
                    self.write(json_encode({"success": False}))

            if i.slevel == 'changePasswd':

                try:
                    reslut_cPw=auth.change_passwd(i.username,i['value[oldPasswd]'],i['value[newPasswd]'])
                    if reslut_cPw == True:
                        self.clear_cookie("user")
                        self.write(json_encode({"success": True}))
                        return True
                    else:
                        self.write(json_encode({"success": False}))
                    return False
                except Exception,e:
                    print(e)
                    self.write(json_encode({"success": False}))
                    return False


##########nmap#########
    @run_on_executor
    def nmapScan(self,obj,args):
        if not args:
            args=' -T4  -sUT   -n '
        return Snmap().nmap_port_sev(obj,arguments=args)
##################################