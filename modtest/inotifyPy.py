#!/usr/bin/python
import os,time
import threading
from sys import getsizeof
import pyinotify

changefiles=[]
changedirs=[]
delfd=[]
main=[]

lock=threading.RLock()
class judgeThread(threading.Thread):
    def __init__(self,obj,mes):
        threading.Thread.__init__(self)
        self.obj=obj
        self.mes=mes
    def run(self):
        global main
        global lock
        if self.obj.endswith('.swp') or self.obj.endswith('.swx'):pass
        else:
            if self.mes =='DELETE':
                #if os.path.isfile(self.obj):
                #    self.obj=os.path.split(self.obj)[-1]
                lock.acquire()
                if self.obj  not in delfd:
                    delfd.append(self.obj)
                lock.release()
            if self.mes == 'CLOSE_WRITE':
                lock.acquire()
                if self.obj not in changefiles:
                    changefiles.append(self.obj)
                lock.release()
            if self.mes == 'CREATE':
                lock.acquire()
                if os.path.isdir(self.obj):
                    oldThread=main.pop(0)
                    t=mainThread()
                    main.append(t)
                    changedirs.append(self.obj)
                    t.start()
                    oldThread.stop()
                    time.sleep(1)
                    print oldThread.isAlive()
                lock.release()



class mainThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.keepRunning = 1
    def run(self):
        mask = pyinotify.IN_DELETE  |pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE
        wm = pyinotify.WatchManager()
        wm.add_watch('/root/test/monitor', mask, rec=True)
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
        print threading.activeCount()
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


class test(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            print('del',delfd)
            print('cdir',changedirs)
            print('cfile',changefiles)
            time.sleep(5)

if __name__ =='__main__':
    t=mainThread()
    ts=test()
    main.append(t)
    main[0].start()
    ts.start()
    print ts.isAlive()



#notifier.loop()








