# -*- coding: utf-8 -*-
__author__ = 'fuqiang'
import ast
from moudle.Mysql_orm import table_operate
table_operate=table_operate()

def AllMasterIP():
    obj=table_operate.getSelf("select * from s_table")
    for i in obj:
        if not i['srv_num']:
            print(i['id'])
    return [srv['srv_num'] for srv in obj  ]

def verifyIp():
    obj=table_operate.getSelf("select * from verify_nmap")
    return [srv for srv in obj ]

port_ignore=[25,110,111]
port_state=['filtered','closed','open|filtered']
def main():
    data={}
    for k in verifyIp():
        if k['srv_num']:
            ad=table_operate.getone("""select admin from s_table
                where srv_num='{0}'""".format(k['srv_num']))
            if ad:
                info=[]
                host={}
                portinfo=[]
                admin=ad['admin']
                host['srv_num']=k['srv_num']
                verifyData=ast.literal_eval(k['nmapdata'])
                for  portk in verifyData:
                    if portk['port'] in port_ignore or portk['state'] in port_state:
                        continue
                    if portk['verify'] == 0:
                        portinfo.append(portk['port'])
                host['port']=portinfo
                info.append(host)
                if admin in data.keys():
                    data[admin]=data[admin] + info
                else:
                    data[admin]=info
    for nmae in data:
        print(data[nmae])




main()