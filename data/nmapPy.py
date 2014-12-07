__author__ = 'fuqiang'

import nmap
import torndb,time
import json
import sys
from utils import *
import threading

reload(sys)
sys.setdefaultencoding('utf-8')
class Snmap():
    def nmap_port_sev(self,ip,arguments=' -T4  -sUT   -n '):
        data={}
        sn=nmap.PortScanner()
        sn.scan(ip,arguments=arguments)
        tcpdata=sn[ip].all_tcp()
        udpdata=sn[ip].all_udp()
        portdict={}
        def pStatus(ip,port,type):
            portstatusdict={}
            portstatusdict['name']=sn[ip][type][port]['name']
            portstatusdict['conf']=sn[ip][type][port]['conf']
            portstatusdict['extrainfo']=sn[ip][type][port]['extrainfo']
            portstatusdict['state']=sn[ip][type][port]['state']
            portstatusdict['product']=sn[ip][type][port]['product']
            portstatusdict['version']=sn[ip][type][port]['version']
            portstatusdict['reason']=sn[ip][type][port]['reason']
            portstatusdict['cpe']=sn[ip][type][port]['cpe']
            return portstatusdict
        for tport in tcpdata:
            tportstatusdict=pStatus(ip,tport,'tcp')
            portdict[tport]=tportstatusdict
        for uport in udpdata:
            uportstatusdict=pStatus(ip,uport,'udp')
            portdict[uport]=uportstatusdict
        data[ip]=portdict
        print data


class mysqlConn():
    def __init__(self):
        self.mysqld = torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)
    def mysqld(self):
        mysqld=self.mysqld
        return mysqld
    def __del__(self):
        self.mysqld.close()
mylock = threading.RLock()
class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global IpDict
        while IpDict:
            mylock.acquire()
            ip=IpDict.pop()
            print ip
            mylock.release()
            Snmap().nmap_port_sev(ip)
sdb=mysqlConn().mysqld

obj=sdb.query("select srv_num from s_table")
IpDict=[]
for key in obj:
    iptmp=(key['srv_num'].split('_')[1]).strip()
    if IsPubIp(iptmp) == True:
        IpDict.append(iptmp)

thread1 = myThread()
thread2 = myThread()
thread3 = myThread()
cstart=time.time()
thread1.start()

thread2.start()
thread3.start()
cend=time.time()

runtime=cend -cstart
print(runtime)