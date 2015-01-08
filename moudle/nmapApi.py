__author__ = 'fuqiang'
import sys,ast
sys.path.append('/data/wwwroot/www.test.com/webroot/web_excel/')
import nmap
import datetime
from utils import *


from moudle import Mysql_orm
from moudle import table_orm
table_operate=Mysql_orm.table_operate()
reload(sys)
sys.setdefaultencoding('utf-8')

class Snmap():
    def nmap_port_sev(self,srvip,arguments=' -T4  -sUT   -n '):
        arguments=str(arguments).strip()
        if IsIpAddr(srvip) == True:
            ip=str(srvip)
        else:
            ip=str(srvip.split('_')[1].strip())
            if IsIpAddr(ip) != True:
                return False
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

        oldVerify=table_operate.getone("""select nmapdata from verify_nmap
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
                table_operate.insert_by_dict('table_nmap',data)
                table_operate.mdb().update_by_dict('verify_nmap',verifydata, "srv_num = '{0:s}'".format(srv_num))
            except Exception,e:
                print(sys.exc_info())
                print(e)
        else:
            try:
                verifydata['srv_num'] =srv_num
                verifydata['nmapdata']=json.dumps(verifyKeys)
                verifydata['opTime'] =str(tmptime)
                table_operate.insert_by_dict('table_nmap',data)
                table_operate.insert_by_dict('verify_nmap',verifydata)
            except Exception,e:
                print(sys.exc_info())
                print(e)
        return {'data':data,'status':True}


