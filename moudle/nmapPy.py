__author__ = 'fuqiang'

import nmap
import torndb,time
import json
import sys
from utils import *
import threading

reload(sys)
sys.setdefaultencoding('utf-8')
myHost='10.0.0.115'
myPort='3306'
myDb='demo2'
myUser='root'
myPasswd='123456'
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

sdb=mysqlConn().mysqld
if __name__ == '__main__':
    obj=sdb.query("select srv_num from s_table")
    IpDict=[]
    for key in obj:
        iptmp=(key['srv_num'].split('_')[1]).strip()
        if IsPubIp(iptmp) == True:
            IpDict.append(iptmp)

    def thnmap(obj):
        for i in obj:
            b=obj.pop()
            print(b)
            print(obj)
            try:
                Snmap().nmap_port_sev(b)
            except Exception,esx:
                print(esx)
                continue
    threads = []
    threads.append(threading.Thread(target=thnmap(IpDict)))
    threads.append(threading.Thread(target=thnmap(IpDict)))
    threads.append(threading.Thread(target=thnmap(IpDict)))
    cstart=time.time()
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    cend=time.time()
    runtime=cend -cstart
    print(runtime)