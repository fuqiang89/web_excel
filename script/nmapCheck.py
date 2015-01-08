__author__ = 'fuqiang'

from moudle.Mysql_orm import table_operate
table_operate=table_operate()

def AllMasterIP():
    obj=table_operate.getSelf("select * from s_table")
    for i in obj:
        if not i['srv_num']:
            print(i['id'])
    return [srv['srv_num'] for srv in obj  ]

def verifyIp():
    obj=table_operate.getSelf("select srv_num from verify_nmap")
    return [srv['srv_num'] for srv in obj ]




