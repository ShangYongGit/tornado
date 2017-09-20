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

class HtmlHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

    def post(self):
        name = self.get_argument('name',' ')
        password = self.get_argument('password',' ')
        self.write('---%s---%s--'%(name,password))

class RequestMyHandler(tornado.web.RequestHandler):
    def get(self):
        print(self.request.method)
        print(self.request.uri)
        print(self.request.path)
        print(self.request.query)
        print(self.request.version)
        print(self.request.headers)
        print(self.request.remote_ip)   #重要点
        print(self.request.request_time)
        print(self.request.full_url)
        print(self.request.cookies)
        print(self.request.host)
        print(dir(self.request))


class HeaderHandler(tornado.web.RequestHandler):
    #def set_default_headers(self):
    def get(self):
        self.set_header('aaa','111')
        self.add_header('ccc','222')
        self.add_header('ccc','333')
        self.clear_header('ccc')
        self.write('abc')

class RedirectHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/json')

class FinishHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello1234')
        #self.finish()
        self.write('45678')

class FlushHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello')
        self.flush()
        time.sleep(5)
        self.write('abcd')

class SendErrorHandler(tornado.web.RequestHandler):
    def get(self):
        self.send_error(200)
#项目入口
if __name__=='__main__':

    #解析命令行参数
    tornado.options.parse_command_line()

    #路由映射
    app = tornado.web.Application(
        handlers=[
            (r'/json',JsonHandler),
            (r'/html',HtmlHandler),
            (r'/request',RequestMyHandler),
            (r'/header',HeaderHandler),
            (r'/redirect',RedirectHandler),
            (r'/finish',FinishHandler),
            (r'/flush',FlushHandler),
            (r'/send_error',SendErrorHandler),
        ],
        template_path='templates',  #模板文件
        static_path='static',   #静态文件
        debug=True,
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()


