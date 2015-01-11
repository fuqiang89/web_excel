# -*- coding: utf-8 -*-
__author__ = 'fuqiang'
import os,sys
import re
import json,ast
import datetime
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
from moudle.mysqlOrm import table_operate
from moudle.sendmail import sendmail
from moudle.twilioCall import CallMs
from moudle.twilioSms import SMS
class apiTst(basehandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
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
            if i.slevel == 'emailTest':
                print(i.email)
                if re.match(r"[^@]+@[^@]+\.[^@]+", i.email):
                    to_users=[]
                    to_users.append(i.email.replace(' ',''))
                    #print(to_users)
                    redata=sendmail.Sendmail(to_users=to_users,subject="邮件测试",
                                      content="this is test mail!")
                    if redata:
                        self.write(json_encode({'result':True}))
                        return
                    else:
                        self.write(json_encode({'result':False}))
                else:
                    self.write(json_encode({'result':False}))
                    return
        if  i.stype == 'account':
            if i.slevel == 'phoneTest':
                if re.match(r"^[1][0-9][0-9]{9}$", i.phone):
                    to_users=i.phone.replace(' ','')
                    redata=CallMs.notify(to_users,"这是一个测试电话！听到这个说明测试成功，哈哈。")
                    if redata:
                        self.write(json_encode({'result':True}))
                        return
                    else:
                        self.write(json_encode({'result':False}))
                else:
                    self.write(json_encode({'result':False}))
                    return
        if  i.stype == 'account':
            if i.slevel == 'smsTest':
                if re.match(r"^[1][0-9][0-9]{9}$", i.phone):
                    to_users=i.phone.replace(' ','')
                    redata=SMS.sms(to_users,"这是一个测试短信！听到这个说明测试成功，哈哈。")
                    if redata:
                        self.write(json_encode({'result':True}))
                        return
                    else:
                        self.write(json_encode({'result':False}))
                else:
                    self.write(json_encode({'result':False}))
                    return