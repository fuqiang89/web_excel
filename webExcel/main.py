__author__ = 'fuqiang'
import tornado.web,tornado.websocket
import random,time
from tornado.escape import json_encode
import tornado.escape
from basehandler import basehandler


class  Socket(tornado.websocket.WebSocketHandler):
    #@tornado.web.authenticated
    def open(self):
        try:
            for i in range(1,100):
                Tim=int(time.time())*1000

                time.sleep(0.5)
                self.write_message(json_encode([Tim,i]))

        except:
            print "close"
        #self.write_message('Welcome to WebSocket')
    def on_message(self, message):
        self.write_message(u"You said: " + message)
    @classmethod
    def on_close(self):
        print("close socket")







class Listcount(basehandler):
    @tornado.web.authenticated
    def get(self):
        i = self.input()
        i.recs=objd.getcount()
        print(i)

        self.render("list.html",i=i)
class Iplist(basehandler):
    @tornado.web.authenticated
    def get(self):
        i=self.input()
        i.recs=objip.getipdata()
        #self.write("web/chart.html")
        #time.sleep(2)
        #self.render("web/test.html",i=i)
        self.render("sock3.html")

        #t1=t.load("iplist.html")
        #htmlt=t1.generate(i=i)
        #self.write(htmlt)