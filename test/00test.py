#导入需要的模块
import tornado.httpserver
import tornado.web
import tornado.ioloop
from tornado.options import  define,options

#定义默认的端口
define('port',default=8000,help="port details",type=int)
define('version',default='v1.0',help='version number',type=int)

#定义一个请求处理逻辑
class IndexHandler(tornado.web.RequestHandler):
    #服务器请求就是get方法
    def get(self):
        self.write('this is test')

class AaaHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('aaa')

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        aaa = self.get_argument('aaa','no')  # no 是默认参数，如果没有的话就是aaa=no 和字典中的get方法一样
        #aaa = self.get_arguments('aaa')  #使用很少
        #print(aaa)  #使用get_arguments返回的是一个列表
        self.write(aaa)

    def post(self):  #post请求
        bbb = self.get_argument('bbb','no')
        self.write(bbb)

#rest 请求
class BookHandler(tornado.web.RequestHandler):
    def get(self,name,age):
        self.write('---name=%s----age=%s'%(name,age))

class BookNameHandler(tornado.web.RequestHandler):
    def get(self,name,age):
        self.write('---name=%s----age=%s'%(name,age))

#项目入口
if __name__=='__main__':

    #解析命令行参数
    tornado.options.parse_command_line()
    #print(options.port)
    #print(options.vesion)

    #路由映射
    app = tornado.web.Application(
        handlers=[
            (r'/abc',IndexHandler),
            (r'/aaa',AaaHandler),
            (r'/hello',HelloHandler),
            (r'/book/(.+)/([1-9]+)',BookNameHandler),#通过url名称不固定的传参
            (r'/bookname/(?P<name>.+)/(?P<age>[1-9]+)',BookNameHandler),

        ]
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()


