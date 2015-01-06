__author__ = 'fuqiang'
import sys
sys.path.append('/root/web_excel/')
import nmap
import torndb,time,datetime
import json
from utils import *
import threading




from moudle import Mysql_orm
from moudle import table_orm
table_operate=Mysql_orm.table_operate()
reload(sys)
sys.setdefaultencoding('utf-8')
myHost='10.0.0.110'
myPort='3306'
myDb='srv_table_test'
myUser='root'
myPasswd='123456'



class Snmap():
    def nmap_port_sev(self,ip,arguments=' -T4  -sUT   -n '):
        tmptime=datetime.datetime.now()
        sdbnmap=mysqlConn().mysqld
        data={}
        verifydata={}
        sn=nmap.PortScanner()
        sn.scan(ip,arguments=arguments)
        tcpdata=sn[ip].all_tcp()
        udpdata=sn[ip].all_udp()
        keys=[]
        verifyKeys=[]

        def pStatus(ip,port,type):
            portstatusdict={}
            verifyPort={}
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
            portstatusdict['verify']=0
            verifyPort['port']=port
            verifyPort['state']=sn[ip][type][port]['state']
            verifyPort['verify']=0
            return portstatusdict,verifyPort
        for tport in tcpdata:
            tportstatusdict,verifyPortTcp=pStatus(ip,tport,'tcp')
            keys.append(tportstatusdict)
            verifyKeys.append(verifyPortTcp)


        for uport in udpdata:
            uportstatusdict,verifyPortUdp=pStatus(ip,uport,'udp')
            keys.append(uportstatusdict)
            verifyKeys.append(verifyPortUdp)



        srv_num='srv_{0}'.format(ip)
        data['srv_num'] =srv_num
        data['nmapdata']=json.dumps(keys)
        data['opTime']=str(tmptime)


        verifydata['srv_num'] =srv_num
        verifydata['nmapdata']=json.dumps(verifyKeys)
        verifydata['opTime'] =str(tmptime)
        try:
            sdbnmap.insert_by_dict('table_nmap',data)
            try:
                sdbnmap.insert_by_dict('verify_nmap',verifydata)
            except Exception,e:
                print(e)

                sdbnmap.update_by_dict('verify_nmap',verifydata,
                                       "srv_num = '{0:s}'".format(srv_num))
        except Exception,e:
            print(sys.exc_info())
            print(e)

        #print data


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
IpDict=['127.0.0.1']
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
