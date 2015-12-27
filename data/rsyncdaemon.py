__author__ = 'Administrator'
import socket, yaml,datetime
import ast
import torndb
import time, os, sys
from rsyncPy import rsync

config_file = 'config.yml'
config_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'conf' + os.sep + config_file

f = open(config_file)
configMap = yaml.load(f)
f.close()

mysqlConfig=configMap['mysql']
target=configMap['target']

def mydb(mysqlConfig):
    return torndb.Connection( '%s:%s'  % (mysqlConfig['address'],mysqlConfig['port']),
                              mysqlConfig['database'],mysqlConfig['user'],mysqlConfig['password'])




def run(mtarget):
    tmptime=str(datetime.datetime.now())
    sdb=mydb(mysqlConfig)
    # data=sdb.query('select * from changeData  where date(opTime)=curdate() - INTERVAL 1 day')
    data=sdb.query("""select * from changeData  where date(opTime)=curdate()
                and type != 'DELETE' and {0}  in ('wait')""".format(mtarget))
    rsyncd=rsync(target[mtarget])
    fileque=[]
    for rdt in data:
        fileque.append(rdt)
    for rdt in fileque:
        status_code=rsyncd.push(rdt)
        if rsyncd.push(rdt):
            try:
                udata={mtarget:'success'}
                sdb.update_by_dict('changeData',udata,'id = {0}'.format(rdt['id']))
            except Exception,e:
                print(e)
                print(rdt,'rsync is ok ,but update status  is failure!')
        else:
            try:
                udata={mtarget:'failure'}
                sdb.update_by_dict('changeData',udata,'id = {0}'.format(rdt['id']))

            except Exception,e:
                print(e)
                print(rdt,'rsync is failure and update status  is failure!')
    sdb.close()



if __name__ == '__main__':
    try:
        mtarget=sys.argv[1]
    except Exception:
        print 'not target!'
        exit(1)

    if mtarget in target.keys():
        pass
    else:
        print 'config.yaml  not target match'
        exit(1)
    try:
        sdb=mydb(mysqlConfig)
        mdata=sdb.query("select COLUMN_NAME from information_schema.COLUMNS where table_name = 'changeData'")
        fields=[]
        for fild_dict in mdata:
            fields.append(fild_dict['COLUMN_NAME'])
        if mtarget not in fields:
            print 'mysql field not target!'
            exit(1)
    except Exception,e:
        print(e)
        print 'mysql connect error!'
        exit(1)
    run(mtarget)
