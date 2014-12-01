__author__ = 'fuqiang'

import nmap
import json

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


if __name__ == '__main__':
    Snmap=Snmap().nmap_port_sev('121.207.240.92')