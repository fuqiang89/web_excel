__author__ = 'fuqiang'
import sys
sys.path.append('/data/wwwroot/www.test.com/webroot/web_excel_150106/web_excel')
import nmap
import torndb,time,datetime
import json,ast,copy
from utils import *
import threading
import time





# from moudle.Mysql_orm import table_operate
from moudle import table_orm
# table_operate=table_operate()
reload(sys)


sys.setdefaultencoding('utf-8')


myHost='172.16.10.101'
myPort='3306'
myDb='srv_table'
myUser='srv_table_user'
myPasswd='srv_table_fuqiang123'



result=[]
resultVerify=[]
resultoldVerify=[]
class Snmap():
    def nmap_port_sev(self,ip,arguments=' -T4  -sUT   -n '):

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
        data['srv_num'] = verifydata['srv_num'] =srv_num
        # data['nmapdata']=json.dumps(keys)
        data['nmapdata']=keys
        data['opTime']= verifydata['opTime'] =str(tmptime)
        verifydata['nmapdata']=verifyKeys
        result.append(data)
        resultVerify.append(verifydata)

        oldVerify=sdbnmap.get("""select nmapdata from verify_nmap
        where srv_num = '{0:s}'""".format(srv_num))
        if oldVerify:
            oldVerifyData=oldVerify['nmapdata']
            oldVerifyData=ast.literal_eval(oldVerifyData)
            resultoldVerify.append(oldVerifyData)
        else:resultoldVerify.append(None)









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
IpDict=[]
for key in obj:
    iptmp=str((key['srv_num'].split('_')[1]).strip())
    if IsPubIp(iptmp) == True:
        IpDict.append(iptmp)
IpDict=['127.0.0.1','121.207.254.248']
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

# olddata=copy.deepcopy(resultoldVerify)
for ok in resultoldVerify:
    if ok is None:
        try:
            row=resultVerify[resultoldVerify.index(ok)]
            row['nmapdata']=json.dumps(row['nmapdata'])
            sdbnmap.insert_by_dict('verify_nmap',row)
            resultoldVerify.remove(ok)
        except Exception,e:
            resultoldVerify.remove(ok)
            print(sys.exc_info())
            print(e)

# for ko in olddata:





# for obj in resultVerify:
#     verifyKeysComparison=[]
#     vports=[]
#     nmapdata=obj['nmapdata']
#     for vk in nmapdata:
#         if vk['verify'] ==1:
#             vports.append(vk['port'])
#     for nk in result[resultVerify.index(obj)]:
#         if nk['port'] in vports:
#             nk['verify'] = 1
#         else:verifyKeysComparison.append(nk)

