__author__ = 'fuqiang'

import nmap
import torndb,time
import json
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
    cstart=time.time()
    ipp=['127.0.0.1','69.59.152.220','115.239.211.110','162.243.87.81']
    for i in ipp:
        print(i)
        #Snmap().nmap_port_sev(i)
    cend=time.time()
    runtime=cend -cstart