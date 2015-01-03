# -*- coding: utf-8 -*-
__author__ = ''
import os,sys,datetime
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
import logging

#tl=template.Loader(os.path.join(TP, "webExcel/srv_html"))
table_operate=table_operate()
table_orm=table_orm()
operate_register=operate_register()




###############
#logging.basicConfig(level=logging.ERROR,
#                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                    datefmt='%a, %d %b %Y %H:%M:%S',
#                    filename="%ssrv_cmd.log" % dataPath,
#                     filemode='a')
#########
class Data(basehandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        i=self.input()
        i.username=self.current_user
        keys=['Fileds','Filter']
        ckeck_keys=set(i.keys()).intersection(set(keys))
        if  len(list(ckeck_keys))!=2:
            ddata=table_operate.getAll()
            for key  in ddata:
                for vk in key:
                    if key[vk]:
                        if vk in ['Srv_used','local_ip','inter_ip','note']:
                            key[vk]= key[vk].replace('/n','<br>')

            self.write(json_encode(ddata))
            return
        if i.Fileds == '':
            Fileds=table_orm.get_fields("srv_table")['fields']
        else:
            Fileds=i.Fileds[:-1].split(':')
        result_data=table_operate.search(i.search,Fileds,i.Filter,'s_table')
        for key  in result_data:
            for vk in key:
                if key[vk]:
                    if vk in ['Srv_used','local_ip','inter_ip','note']:
                        key[vk]= key[vk].replace('/n','<br>')
        self.write(json_encode(result_data))

class  Tg(basehandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        i=self.input()
        i.username=self.current_user
        i.fields=table_orm.get_fields("srv_table")
        self.render("xtable.html",i=i)


class List(basehandler):
    @tornado.web.authenticated
    def get(self):
        i=self.input()
        i.username=self.current_user
        i.fields=table_orm.get_fields("srv_table")
        self.render("xtable.html",i=i)
    def post(self):
        pass
#class Fileds(basehandler):
#    @tornado.web.authenticated
#    def get(self, *args, **kwargs):
#        i=self.input()
#        i.username=self.current_user
#        i.fields=table_orm.get_fields('srv_table')
#        self.write(json_encode(i))



class Update(basehandler):
    @tornado.web.authenticated
    def get(self):
        fields=table_orm.get_fields("srv_table")['fields']
        i=self.input()
        i.username=self.current_user
        i.recs=InitStorage(i,fields)
        i.recs=table_operate.getEntityById(i.id)
        if i.recs:
            for keys  in i.recs:
                if keys in ['Srv_used','local_ip','inter_ip','note']:
                    #if isinstance(i.recs[keys],str):
                    if i.recs[keys]:
                        i.recs[keys]= i.recs[keys].replace('/n',r'\n')
        i.fields=table_orm.get_fields("srv_table")
        i.useAdmin=table_orm.get_useAdmin("srv_table")
        self.render("Upload_xtable.html",i=i)


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
        v=CopyData_INC(v,i,fields)
        try:
            if i.act=="add":
                #vv=valid(v)
                vv=True
                if vv==True:
                    rv=table_orm.replace(v,fields,type='in')
                    redata=table_operate.insert(rv)
                    try:
                        operate_register.reg_add_update(v,'s_table','add',i.username,i.xExplain)
                    except Exception, exc:
                        print(sys.exc_info())
                        print(str(exc))

                    self.write(JsonResult(str(redata)))

                else:
                    self.write(JsonResult("%s  add error!!!" % str(vv)))

            if i.act=="update":
                #vv=valid(v)
                vv=True
                if vv==True:
                    rv=table_orm.replace(v,fields,type='in')
                    redata=table_operate.update(rv)
                    try:
                        #print(i.xExplain)
                        operate_register.reg_add_update(v,'s_table','update',i.username,i.xExplain)
                    except Exception, exc:
                        print(sys.exc_info())
                        print(str(exc))

                    self.write(json_encode({'result':str(redata)}))
                else:
                    self.write(json_encode({'result':"update error!"}))
            if i.act=="del":
                try:
                    operate_register.reg_del(i.id,'s_table',fields,i.username,i.xExplain)

                except Exception, exc:
                    print(i)
                    print(str(exc))
                try:
                    table_operate.delEntityById(i.id)
                    self.write(JsonResult('True'))
                    return
                except Exception,e:
                    self.write(JsonResult(str(e)))
                    return
        except Exception, exc:
            print(sys.exc_info())
            self.write(JsonResult("%s" % str(exc)))



class postWebData(basehandler):
    def get(self, *args, **kwargs):
        pass
    def post(self, *args, **kwargs):
        args=self.input()
        fields=table_orm.get_fields("srv_table")['fields']
        rs=table_orm.exportExecl_json(fields,args['postdata'])
        self.write(rs)
class downLoad(basehandler):
    def get(self, *args, **kwargs):
        args=self.input()
        fname=dataPath+args['fname']
        try:
            with open(fname, 'rb') as f:
                self.set_header ('Content-Type', 'text/xlsx')
                self.set_header ('Content-Disposition', 'attachment; filename=%s' % args['fname'])
                self.write(f.read())
                self.finish()
        except Exception,exc:
            pass


class xProfile(basehandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        i=self.input()
        try:
            i.id=table_operate.getEntityBySrv_num(i.srv_num)['id']
        except Exception:
            #self.render('page_500.html')
            i.id=table_operate.getSelf('select max(id) as id from s_table')[0]['id']

        i.username=self.current_user
        self.render("xProfile.html",i=i)

#