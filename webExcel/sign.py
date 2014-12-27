__author__ = 'fuqiang'

from basehandler import basehandler

from moudle.accountMod import Authentication
Auth=Authentication()
class LoginHandler(basehandler):
    def get(self):
        self.render("login.html")
    def post(self):
        i=self.input()
        #Alldata = self.request.arguments
        #username = self.get_argument("username", "")
        #password = self.get_argument("password", "")
        username=i.username
        password=i.password
        authmes = Auth.userAuth(username,password)
        result_auth=authmes[0]
        result_login_status=authmes[1]
        if result_auth == True:
            if result_login_status == 0:
                self.set_secure_cookie("user",username,expires_days=0.123)
                self.redirect(self.get_argument('next', '/xtable'))
            if result_login_status != 0:
                self.set_secure_cookie("user",username,expires_days=0.123)
                self.render('userinfo.html',i=i)
        else:
            self.render("login.html")
class LogoutHandler(basehandler):
    def get(self):
        if not self.get_current_user():
            self.redirect('/')
            return
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))