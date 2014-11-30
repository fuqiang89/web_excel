__author__ = 'fuqiang'

from basehandler import basehandler
class LoginHandler(basehandler):
    def get(self):
        self.render("login.html")
    def post(self):
        Alldata = self.request.arguments
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        #authmes = authmongo.Authuser(name=username,passwd=password)
        #print authmes
        if username == 'test' and password == 'test1':
            authmes = True
        else:
            authmes = False
        if authmes == True:
            self.set_secure_cookie("user",username,expires_days=0.123)
            self.redirect(self.get_argument('next', '/'))
        else:
            self.render("login.html")
class LogoutHandler(basehandler):
    def get(self):
        if not self.get_current_user():
            self.redirect('/')
            return
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))