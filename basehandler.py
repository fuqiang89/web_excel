# -*- coding: utf-8 -*-
import json
from tornado.web import RequestHandler
from Storage import storage
class basehandler(RequestHandler):
    #"检查cookie"
    def get_current_user(self):
        return self.get_secure_cookie("user")
    #所有Handler基类
    def input(self):
        #"""获取到所有的输入数据，将其转换成storage方便调用"""
        i= storage()
        #得到所有的输入参数和参数值
        args=self.request.arguments
        for a in args:
            i[a]=self.get_argument(a)
        i["files"]=storage(self.request.files)
        i["path"]=self.request.path
        i["headers"]=storage(self.request.headers)
        return i