__author__ = 'fuqiang'
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line

from webExcel import sign
from webExcel import srv_cmd

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/",srv_cmd.Tg),
            (r"/data",srv_cmd.Data),
            (r"/postData",srv_cmd.postWebData),
            (r"/dl",srv_cmd.downLoad),
            (r"/test",srv_cmd.Fileds),
            (r"/xtable",srv_cmd.List),
            (r"/update",srv_cmd.Update),
            (r"/login",sign.LoginHandler),
            (r"/logout",sign.LogoutHandler)
        ]
        settings = dict(
            cookie_secret="61oETzKXQAGaYdkL5gUYGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,

        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888,address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
if __name__ == '__main__':
    main()
