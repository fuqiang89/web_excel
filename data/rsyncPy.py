__author__ = 'Administrator'
import subprocess,os
import functools

def catchException(fun):
    @functools.wraps(fun)
    def wap(*args,**kwargs):
        try:
            return fun(*args,**kwargs)
        except Exception,e:
            print(e)
            return False
    return wap
class rsync:
    @catchException
    def __init__(self,options):
        self.ip=options['ip']
        self.tag=options['tag']
        self.parameter=options['parameter']
        self.user=options['user']
        try:
            self.password_file=options['password_file']
        except Exception,e:
            self.password_file=''
        if options['delete']:
            self.delete='--delete'
        else:
            self.delete=''


    @catchException
    def push(self,obj):
        # if os.path.isfile(obj) != True:
        #     return False
        tag_map = dict((v,k) for k, v in self.tag.iteritems())
        path=obj['filepath']
        tag=False
        tagPath=False
        for tagvalue in  self.tag.values():
            if path.startswith(tagvalue):
                tag=tag_map[tagvalue]
                tagPath=tagvalue
                break
        if tag and tagPath:
            fs=path.split(tag)
            if len(fs) !=2:
                raise "{0}--{1}filepath split error!".format(obj['id'],path)
            spath=fs[1][1:]
            cmd=["""sh -c 'cd {0} && rsync {1} {7} {2} {3}@{4}::{5} --password-file={6}'""".format(tagPath,self.parameter,
                                                                      spath,self.user,self.ip,tag,self.password_file,self.delete)]
            # cmd=['cd',tagPath,'&&', 'rsync',self.parameter,spath,'{0}@{1}::{2}'.format(self.user,self.ip,tag), '--password-file=/etc/rsync.pass']
            print(cmd)
            p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            out=p.communicate()
            retcode = p.wait()
            if retcode > 0:
                print(obj['id'],path,'rsync is error!')
                for info in out:
                    print(info)
                return False
            return True


        #
        # cmd=['rsync',self.parameter,path,'{0}@{1}::{2}'.format(self.user,self.ip,self.tag)]
        # print(cmd)
