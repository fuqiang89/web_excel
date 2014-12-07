__author__ = 'fuqiang'
import sys
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

        if IsIpAddr(srvip) == True:
            ip=srvip
        else:
            ip=srvip.split('_')[1].strip()
            if IsIpAddr(ip) != True:
                return {'status':False}
        tmptime=datetime.datetime.now()
        data={}
        try:

            sn=nmap.PortScanner()
            sn.scan(ip,arguments=arguments)

            tcpdata=sn[ip].all_tcp()
            udpdata=sn[ip].all_udp()
        except Exception:
            return {'status':False}
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
            table_operate.insert_by_dict('table_nmap',data)
        except Exception,e:
            print(e)
        return {'data':data,'status':True}


