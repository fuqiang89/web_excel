__author__ = 'fuqiang'
import sys
sys.path.append('/data/wwwroot/www.test.com/webroot/web_excel/')
import nmap
import torndb,time,datetime
import json
from utils import *
import threading




from moudle import srv_m
from moudle import table_orm
table_operate=srv_m.table_operate()
reload(sys)
sys.setdefaultencoding('utf-8')
myHost='172.16.10.101'
myPort='3306'
myDb='srv_table'
myUser='srv_table_user'
myPasswd='srv_table_fuqiang123'



class Snmap():
    def nmap_port_sev(self,ip,arguments=' -T4  -sUT   -n '):
        tmptime=datetime.datetime.now()
        sdbnmap=mysqlConn().mysqld
        data={}
        sn=nmap.PortScanner()
        sn.scan(ip,arguments=arguments)
        tcpdata=sn[ip].all_tcp()
        udpdata=sn[ip].all_udp()
        keys=[]

        def pStatus(ip,port,type):
            portstatusdict={}
            portstatusdict['ntype']=type
            portstatusdict['nport']=port
            portstatusdict['name']=str(sn[ip][type][port]['name'])
            portstatusdict['conf']=str(sn[ip][type][port]['conf'])
            portstatusdict['extrainfo']=sn[ip][type][port]['extrainfo']
            portstatusdict['state']=sn[ip][type][port]['state']
            portstatusdict['product']=sn[ip][type][port]['product']
            portstatusdict['version']=sn[ip][type][port]['version']
            portstatusdict['reason']=sn[ip][type][port]['reason']
            portstatusdict['cpe']=sn[ip][type][port]['cpe']
            return portstatusdict
        for tport in tcpdata:
            tportstatusdict=pStatus(ip,tport,'tcp')
            keys.append(tportstatusdict)


        for uport in udpdata:
            uportstatusdict=pStatus(ip,uport,'udp')
            keys.append(uportstatusdict)



        data['srv_num']='srv_%s' % ip
        data['nmapdata']=json.dumps(keys)
        data['opTime']=str(tmptime)
        try:
            sdbnmap.insert_by_dict('table_nmap',data)
        except Exception,e:
            print(e)

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
            print ip,len(IpDict)
            mylock.release()
            try:
                Snmap().nmap_port_sev(ip)
            except Exception,e:
                print(ip + " is nmap error  ")
                continue
sdbnmap=mysqlConn().mysqld

obj=sdbnmap.query("select srv_num from s_table")
IpDict=[]
for key in obj:
    iptmp=str((key['srv_num'].split('_')[1]).strip())
    if IsPubIp(iptmp) == True:
        IpDict.append(iptmp)
Snmap().nmap_port_sev('127.0.0.1')
cstart=time.time()
therd={}
for i in range(200):
    therd[i]=myThread()

for Start in therd:
    therd[Start].start()
for Join in therd:
    therd[Join].join()
cend=time.time()

runtime=cend -cstart
print(runtime)

# thread1 = myThread()
# thread2 = myThread()
# thread3 = myThread()
# thread4 = myThread()
# thread5 = myThread()
# thread6 = myThread()
# thread7 = myThread()
# thread8 = myThread()
# thread9 = myThread()
# thread10 = myThread()
#
# cstart=time.time()
# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()
# thread5.start()
# thread6.start()
# thread7.start()
#
# thread8.start()
# thread9.start()
# thread10.start()
#
# thread1.join()
# thread2.join()
# thread3.join()
# thread4.join()
# thread5.join()
# thread6.join()
# thread7.join()
#
# thread8.join()
# thread9.join()
# thread10.join()
#
# cend=time.time()
#
# runtime=cend -cstart
# print(runtime)