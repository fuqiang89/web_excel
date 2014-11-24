# -*- coding: utf-8 -*-
__author__ = ''
import os,sys
from tornado import template
import tornado.web
from Storage import storage
from utils import *
from tornado.escape import json_encode
from basehandler import basehandler
from config import TP
from moudle.srv_m import table_operate
from moudle.table_orm import table_orm
from moudle.operate_register import operate_register

tl=template.Loader(os.path.join(TP, "webExcel/srv_html"))
table_operate=table_operate()
table_orm=table_orm()
operate_register=operate_register()

class List(basehandler):
    @tornado.web.authenticated
    def get(self):
        i=self.input()
        #print(i.username)
        i.fields=table_orm.get_fields("srv_table")
        t=tl.load("exl_table.html")
        htmlsrc=t.generate(i=i)
        self.write(htmlsrc)
    def post(self):
        pass

class Data(basehandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        ddata=table_operate.getAll()
        for i  in ddata:
            for ii in i:
                if ii in ['Srv_used','local_ip','inter_ip']:
                    i[ii]= i[ii].replace('\\n','<br>')
        self.write(json_encode(ddata))
class Fileds(basehandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        i=self.input()
        i.fields=table_orm.get_fields('srv_table')
        self.write(json_encode(i))

#class Search(basehandler):
#    def get(self):
#        i=self.input()
#        if i.s_keys:
#            i.recs=optobj.search(i.s_keys)
#        else:
#            i.recs=optobj.getAll()
#        t=tl.load("srvlist.html")
#        #t=tl.load("new.html")
#        htmlsrc=t.generate(i=i)
#        self.write(htmlsrc)
#


class Update(basehandler):
    @tornado.web.authenticated
    def get(self):
        fields=table_orm.get_fields("srv_table")['fields']
        i=self.input()
        i.recs=InitStorage(i,fields)
        i.recs=table_operate.getEntityById(i.id)
        i.fields=table_orm.get_fields("srv_table")
        i.useAdmin=table_orm.get_useAdmin("srv_table")
        #i.s_keys=""
        t=tl.load("srv_update.html")
        htmlsrc=t.generate(i=i)
        self.write(htmlsrc)

    def post(self):

        fields=table_orm.get_fields("srv_table")['fields']
        def valid(v):
            if v.inter_ip:
                for inter_ip in v.inter_ip.split(','):
                    if IsIpAddr(inter_ip):
                        pass
                    else:
                        return inter_ip
            if v.local_ip:
                for local_sip in v.local_ip.split(','):
                    if IsIpAddr(local_sip):
                        pass
                    else:
                        return local_sip
            return True
        self.set_header("Content-Type", "application/json")
        v=storage()
        i=self.input()
#        i.s_keys=""
        v=CopyData_INC(v,i,fields)
        try:
            if i.act=="add":
                #vv=valid(v)
                vv=True
                if vv==True:
                    table_operate.insert(v)
                    #try:
                    #    operate_register.reg_add(v,'s_table','add')
                    #except Exception, exc:
                    #    print(sys.exc_info())
                    #    print(str(exc))
                    self.write(JsonResult("OK"))

                else:
                    self.write(JsonResult("%s       error!!!" % str(vv)))

            if i.act=="update":
                #vv=valid(v)
                vv=True
                if vv==True:
                    table_operate.update(v)
                    #try:
                    #    operate_register.reg_add(v,'s_table','update')
                    #except Exception, exc:
                    #    print(sys.exc_info())
                    #    print(str(exc))
                    self.write(JsonResult("OK"))
                else:
                    self.write(JsonResult("      %s       error!!!" % str(vv)))
            if i.act=="del":
                #try:
                #    operate_register.reg_del(i.id,'s_table',fields)
                #except Exception, exc:
                #    print(sys.exc_info())
                #    print(str(exc))
                table_operate.delEntityById(i.id)

                self.write(JsonResult("OK"))
        except Exception, exc:
            print(sys.exc_info())
            self.write(JsonResult("%s" % str(exc)))



