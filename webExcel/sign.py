__author__ = 'fuqiang'

from basehandler import basehandler
#from moudle.mongo import Passwdmongo
#authmongo = Passwdmongo()

class LoginHandler(basehandler):
    def get(self):
        self.render("login.html")
    def post(self):
        Alldata = self.request.arguments
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        #authmes = authmongo.Authuser(name=username,passwd=password)
        #print authmes
        authmes = True
        if authmes == True:
            self.set_secure_cookie("user", username,expires_days=0.123)
            self.redirect("/")
        else:
            self.render("login.html")