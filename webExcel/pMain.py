# -*- coding: utf-8 -*-
__author__ = ''
import os,sys
from tornado import template
from tornado.web import RequestHandler
import tornado.web,tornado.websocket
import random,time
import tornado.escape
import tornado.web
from Storage import storage
from utils import *
from tornado.escape import json_encode
from basehandler import basehandler
from config import TP
from moudle.mysqlOrm import table_operate
from moudle.tableOrm import table_orm
from moudle.operateRegister import operate_register
from config import dataPath

table_operate=table_operate()
table_orm=table_orm()
operate_register=operate_register()
class Dashboard(basehandler):
    @tornado.web.authenticated
    def get(self):
        i=self.input()
        i.username=self.current_user
        i.fields=table_orm.get_fields("srv_table")
        self.render("index.html",i=i)
    def post(self):
        pass

class history(basehandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        i=self.input()
        i.username=self.current_user
        i.fields=table_orm.get_fields("srv_table")
        self.render("history.html",i=i)
    def post(self):
        pass


class nmap(basehandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        i=self.input()
        i.username=self.current_user
        self.render("nmap.html",i=i)
    def post(self):
        pass


class monitor(basehandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        i=self.input()
        i.username=self.current_user
        if 'ui_ajax' in i.values():
            self.render("sub/ui_ajax.html",i=i)

        else:
            self.render("monitor.html",i=i)
    def post(self, *args, **kwargs):
        pass
class myProfile(basehandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        i=self.input()
        i.username=self.current_user
        self.render('user/account_info.html',i=i)
    def post(self, *args, **kwargs):
        pass
#class  Socket(tornado.websocket.WebSocketHandler):
#    @tornado.web.authenticated
    #def open(self):
    #    try:
    #        for i in range(1,100):
    #            Tim=int(time.time())*1000
    #
    #            time.sleep(0.5)
    #            self.write_message(json_encode([Tim,i]))
    #
    #    except:
    #        print "close"
    #    self.write_message('Welcome to WebSocket')
    #def on_message(self, message):
    #    self.write_message(u"You said: " + message)
    #@classmethod
    #def on_close(self):
    #    print("close socket")
#
#