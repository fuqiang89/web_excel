#!/usr/bin/python
import os,time,datetime
import threading
import  functools
from sys import getsizeof
import pyinotify



import torndb
#myHost='172.16.10.101'
#myPort='3306'
#myDb='rsyncdb'
#myUser='srv_table_user'
#myPasswd='srv_table_fuqiang123'

myHost='172.16.10.101'
myPort='3306'
myDb='rsyncdb'
myUser='srv_table_user'
myPasswd='srv_table_fuqiang123'

main=[]
def checkfile(obj):
    suffix_list=['.apk']
    ignore_suffix_list=['.swx','.swpx','.swp']
    for ignore_suffix in ignore_suffix_list:
        if obj.endswith(ignore_suffix):
            return False
    for suffix in suffix_list:
        if obj.endswith(suffix):
            return True
    return False



def catchException(fun):
    @functools.wraps(fun)
    def wap(*args,**kwargs):
        try:
            return fun(*args,**kwargs)
        except Exception,e:
            print(e)
            return False
    return wap


lock=threading.RLock()
class judgeThread(threading.Thread):
    def __init__(self,obj,mes):
        threading.Thread.__init__(self)
        self.obj=obj
        self.mes=mes
    @catchException
    def run(self):
        global lock,checkfile
        if checkfile(self.obj) == False:
            return
        sdb=torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)
        tmptime=str(datetime.datetime.now())
        update={'opTime':tmptime}
        update['filepath']=self.obj
        if self.mes =='DELETE':
            update['type']='DELETE'
            sdb.insert_by_dict('changeData',update)
            sdb.close()
        if self.mes == 'CLOSE_WRITE':
            update['type']='CLOSE_WRITE'
            sdb.insert_by_dict('changeData',update)
            sdb.close()
            return






class mainThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.keepRunning = 1
    @catchException
    def run(self):
        global EventHandler
        mask = pyinotify.IN_DELETE  |pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE
        wm = pyinotify.WatchManager()
        wm.add_watch('/data/ftp/upload.get5.com/soft', mask, rec=True,auto_add=True)
        notifier = pyinotify.Notifier(wm, EventHandler())
        while self.keepRunning:
            try:
                notifier.process_events()
                if notifier.check_events():
                    notifier.read_events()
            except KeyboardInterrupt:
                    notifier.stop()
                    break
    def stop(self):
        self.keepRunning = 0

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_DELETE(self, event):
        global judgeThread
        t=judgeThread(event.pathname,'DELETE')
        t.start()
    def process_IN_CREATE(self, event):
        global judgeThread
        t=judgeThread(event.pathname,'CREATE')
        t.start()
    def process_IN_CLOSE_WRITE(self, event):
        global judgeThread
        t=judgeThread(event.pathname,'CLOSE_WRITE')
        t.start()
class monit(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    @catchException
    def run(self):
        global main
        global mainThread
        while True:
            time.sleep(1)
            if main[0].isAlive() == False:
                main=[]
                t=mainThread()
                main.append(t)
                main[0].start()

class test(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    @catchException
    def run(self):
        global main
        a=1
        while True:
            print('status',main[0].isAlive(),threading.activeCount(),main[0])
            time.sleep(5)
            print(a)
            a=a+1

if __name__ =='__main__':
    t=mainThread()
    main.append(t)
    ts=test()
    monit=monit()
    main[0].start()
    ts.start()
    monit.start()




#notifier.loop()



#class newdirThread(threading.Thread):
#    def __init__(self,obj):
#        threading.Thread.__init__(self)
#        self.obj=obj
#    @catchException
#    def run(self):
#        global lock,checkfile
#        sdb=sdb=torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)
#        tmptime=str(datetime.datetime.now())
#        update={'opTime':tmptime}
#        for path, dirs, files in os.walk(self.obj):
#            for fs in files:
#                filepath=os.path.join(path, fs)
#                if checkfile(filepath) == False:
#                    continue
#                update['filepath']=filepath
#                sdb.insert_by_dict('changeData',update)
#        sdb.close()




