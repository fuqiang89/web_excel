# -*- coding: utf-8 -*-
__author__ = 'fuqiang'
import ast
import sys
sys.path.append('/data/wwwroot/www.test.com/webroot/web_excel_150112/web_excel')
from script.sendmail import Mail
from moudle.mysqlOrm import table_operate
table_operate=table_operate()
sendmail=Mail()
def AllMasterIP():
    obj=table_operate.getSelf("select * from s_table")
    for i in obj:
        if not i['srv_num']:
            print(i['id'])
    return [srv['srv_num'] for srv in obj  ]

def verifyIp():
    obj=table_operate.getSelf("select * from verify_nmap")
    return [srv for srv in obj ]

def getMail(obj):

    try:
        key=obj.keys()
        # print(key)
        if len(key) ==1:
            value=str(obj[key[0]])

        else: return None
    except Exception,e:
        return None
    sql="""select mail from account where   {0} = '{1}'""".format(key[0],value)
    return table_operate.getone(sql)



port_ignore=[8000, 8008, 8081, 8090, 8099, 8100,3001,443,53, 123,5989, 8089, 161,2049, 8089, 161,\
             2049,25,110,111,80, 143, 465, 587, 873, 993,\
             995, 1099, 1311, 2200, 2301, 5666, 8002, \
             8031, 8042, 8088, 8888, 9002,4000, 4001, 4002, 4003, 4004,8083,5353]
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
    for admin in data:
        to_users=[]
        email=getMail({'name':admin})
        if email:
            email=email['mail']
            to_users.append(email)
        if data[admin]:
            content='<br>'
            for recond in data[admin]:
                if recond['port']:
                    content=content+'<h1><font size="2" face="arial" ' \
                                'color="blue">{0}</font></h1>'.format(recond['srv_num'])
                    content=content+str(recond['port']) +'<br>'
        if to_users:
            sendmail.Sendmail(to_users=to_users,subject="ports check",content=content)







main()