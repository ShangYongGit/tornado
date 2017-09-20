#导入需要的模块
import json
import time
import tornado.httpserver
import tornado.web
import tornado.ioloop
from tornado.options import  define,options

#定义默认的端口
define('port',default=8000,help="port details",type=int)

#定义一个请求处理逻辑
class JsonHandler(tornado.web.RequestHandler):
    #服务器请求就是get方法
    def get(self):
        di_a = {
            'a':'bb',
            '1':[1,2,3],
        }
        li_b = [1,2,3]
        li_b = json.dumps(li_b)
        li_b = json.dumps(li_b)
        self.write(li_b)

class SendErrorHandler(tornado.web.RequestHandler):
    #def get(self):
    def get(self):
        self.send_error(200, a='abcd')
        # try:
        #     self.send_error(200,a='abcd')
        # except Exception as e:
        #     pass
        #     #send_error_message(e)
    def write_error(self, status_code, **kwargs):
        print(status_code)
        print(kwargs)
        self.write('error')

class CookiesHandler(tornado.web.RequestHandler):
    def get(self):
        # self.set_cookie('aaa','3333333',expires=time.time()+60)
        # self.set_cookie('aaa','3333333',expires_days=1)
        # self.set_cookie('aaa','11111',path='/cookie')  #使用 / ，当前所有的都可以得到这个cookie
        # self.set_cookie('aaa', '11111', httpOnly=False)  #js 不能获取cookies
        # self.set_cookie('bbb', '22222', max_age=60)
        self.set_secure_cookie('ccc','33333')
        # print(self.get_cookie('aaa'))
        self.write('OK')

class Cookies2Handler(tornado.web.RequestHandler):
    def get(self):
        coo = self.get_cookie('aaa')
        print(coo)
        self.write('OK')

#项目入口
if __name__=='__main__':

    #解析命令行参数
    tornado.options.parse_command_line()

    #路由映射
    app = tornado.web.Application(
        handlers=[
            (r'/send_error',SendErrorHandler),
            (r'/cookies',CookiesHandler),
            (r'/cookie2',Cookies2Handler),
        ],
        template_path='templates',  #模板文件
        static_path='static',   #静态文件
        debug=True,  #生产下绝对不允许出现
        cookie_secret='abcd',  #密钥
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()


