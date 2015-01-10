__author__ = 'fuqiang'
from passlib.hash import pbkdf2_sha256
import torndb
from config import *

#hash = pbkdf2_sha256.encrypt("test", rounds=5001, salt_size=16)
#print(hash)
#print(pbkdf2_sha256.verify("test", hash))

class Authentication:
    def __init__(self):
        self.sdb=torndb.Connection( '%s:%s'  % (myHost,myPort),myDb,myUser,myPasswd)
    def __del__(self):
        self.sdb.close()
    def userAuth(self,username,passwd):
        if  (username and passwd):
            pass
        else:
            return False
        try:
            m_data=self.sdb.get("""select * from account
                        where del=0 and username='{0}'""".format(username))
            m_passwd=m_data['passwd']
            first_login=m_data['first_login']
            if not m_passwd:
                return False
            m_passwd=r'$pbkdf2-sha256$5001$'+ m_passwd
            return (pbkdf2_sha256.verify(passwd, m_passwd),first_login)
        except Exception,e:
            print(e)
            return 'unknown'
    def add_account(self,username,passwd,phone=None,mail=None,update=False,**kwargs):
        if  (username and passwd):
            pass
        else:
            return False
        try:
            ent={}
            m_hash = pbkdf2_sha256.encrypt(passwd, rounds=5001, salt_size=16)\
                .replace(r'$pbkdf2-sha256$5001$','')
            ent['passwd']=m_hash
            ent['username']=username
            if update == True:
                ent['first_login']=0
                self.sdb.update_by_dict('account',ent,"username='{0}'".format(username))
            else:
                self.sdb.insert_by_dict('account',ent)
            return True
        except Exception,e:
            print(e)
            return False
    def change_passwd(self,username,old_passwd,new_passwd):
        auth=self.userAuth(username,old_passwd)
        if auth[0] ==True:
            try:
                self.add_account(username,new_passwd,update=True)
                return True
            except Exception,e:
                print(e)
                return False
        else:
            return False
    def change_username(self,username,new_username):
        try:

            m_data=self.sdb.get("""select * from account
                        where del=0 and username='{0}'""".format(username))
            if m_data:
                newDict={'username':new_username}
                self.sdb.update_by_dict('account',newDict,"username = '{0}'".format(username))
                return True
        except Exception,e:
            print(e)
            return False
    def change_email(self,username,new_email):
        try:
            m_data=self.sdb.get("""select * from account
                        where del=0 and username='{0}'""".format(username))
            if m_data:
                newDict={'mail':new_email}
                self.sdb.update_by_dict('account',newDict,"username = '{0}'".format(username))
                return True
        except Exception,e:
            print(e)
            return False

#if __name__ == "__main__":
#    dd=Authentication()
#    #print(dd.userAuth('ttt','gg'))
#    print(dd.add_account('dd','dd'))