__author__ = 'fuqiang'
import sys
sys.path.append('/data/wwwroot/www.test.com/webroot/web_excel_150106/web_excel')
import nmap
import torndb,time,datetime
import json,ast
from utils import *
import threading
import time





# from moudle.Mysql_orm import table_operate
# from moudle import table_orm
# table_operate=table_operate()
reload(sys)


sys.setdefaultencoding('utf-8')


myHost='172.16.10.101'
myPort='3306'
myDb='srv_table'
myUser='srv_table_user'
myPasswd='srv_table_fuqiang123'



class Snmap():
    def nmap_port_sev(self,ip,arguments=' -T4  -sUT   -n '):
        sdb=torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)

        tmptime=datetime.datetime.now()
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

        oldVerify=sdb.get("""select nmapdata from verify_nmap
        where srv_num = '{0:s}'""".format(srv_num))


        vports=[]
        verifyKeysComparison=[]


        if oldVerify:
            oldVerifyData=oldVerify['nmapdata']
            oldVerifyData=ast.literal_eval(oldVerifyData)
            for vk in oldVerifyData:
                if vk['verify'] == 1:
                    vports.append(vk['port'])
            for nk in verifyKeys:
                if nk['port'] in vports:
                    nk['verify'] = 1
                    verifyKeysComparison.append(nk)
                else:verifyKeysComparison.append(nk)
            try:
                verifydata['srv_num'] =srv_num
                verifydata['nmapdata']=json.dumps(verifyKeysComparison)
                verifydata['opTime'] =str(tmptime)
                sdb.insert_by_dict('table_nmap',data)
                sdb.update_by_dict('verify_nmap',verifydata, "srv_num = '{0:s}'".format(srv_num))
            except Exception,e:
                print(sys.exc_info())
                print(e)
        else:
            try:
                verifydata['srv_num'] =srv_num
                verifydata['nmapdata']=json.dumps(verifyKeys)
                verifydata['opTime'] =str(tmptime)
                sdb.insert_by_dict('table_nmap',data)
                sdb.insert_by_dict('verify_nmap',verifydata)
            except Exception,e:
                print(sys.exc_info())
                print(e)
        sdb.close()




        # try:
        #     sdbnmap.insert_by_dict('table_nmap',data)
        #     try:
        #         sdbnmap.insert_by_dict('verify_nmap',verifydata)
        #     except Exception,e:
        #         print(e)
        #
        #         sdbnmap.update_by_dict('verify_nmap',verifydata,
        #                                "srv_num = '{0:s}'".format(srv_num))
        # except Exception,e:
        #     print(sys.exc_info())
        #     print(e)

        #print data


class mysqlConn():
    def __init__(self):
        self.mysqld = torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)
    def mysqld(self):
        mysqld=self.mysqld
        return mysqld


mylock = threading.RLock()
class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global IpDict
        while IpDict:
            mylock.acquire()
            ip=str(IpDict.pop())
            print ip,len(IpDict)
            mylock.release()
            try:
                Snmap().nmap_port_sev(ip)
                time.sleep(5)
            except Exception,e:
                print(e)
                print(sys.exc_info())
                print(ip + " is nmap error  ")
                continue
sdbnmap=mysqlConn().mysqld

obj=sdbnmap.query("select srv_num from s_table")
sdbnmap.close()
IpDict=[]
for key in obj:
    iptmp=str((key['srv_num'].split('_')[1]).strip())
    if IsPubIp(iptmp) == True:
        IpDict.append(iptmp)

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

