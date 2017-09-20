# 导入需要的模块
import json
import time
import tornado.web
import tornado.ioloop
import tornado.httpserver
from pycket.session import SessionMixin
from tornado.options import  define,options

# 定义默认的端口
define('port',default=8000,help="port details",type=int)


class BaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        id = self.get_cookie("ID")
        id = self.session.get('user ')
        return id if id else None #三目运算符

# 定义一个请求处理逻辑
class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        self.write('index登录成功')


class UserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("user登录成功")


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        next = self.get_argument('next','')  #/ 的 url编码就是%2F
        print(next)
        # self.render('login.html',nextname=next)
        self.render('login.html',nextname = self.get_argument("next", ""))

    def post(self):
        name = self.get_argument('name','')
        password = self.get_argument('password','')
        next =  self.get_argument('aaa','')
        print('aaa**',next)
        if name == 'aaa' and password == '111':
            # self.set_cookie('ID',name, max_age=20)
            self.set_secure_cookie("aaa", "bbb")
            self.session.set('user',name)
            self.write('登录成功！')
            # self.redirect(next)
            self.redirect(self.get_argument("aaa", ""))
        else:
            self.write('登陆失败！')


# 项目入口
if __name__ == '__main__':

    # 解析命令行参数
    tornado.options.parse_command_line()

    # 路由映射
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/login', LoginHandler),
            (r'/user', UserHandler),

        ],
        template_path='templates',  # 模板文件
        static_path='static',   # 静态文件
        debug=True,  # 生产下绝对不允许出现
        cookie_secret='aaa',
        login_url='/login',   #如果authenticated验证不通过，则导向这里
        # pycket的配置信息
        pycket = {
            'engine': 'redis',  # 设置存储器类型
            'storage': {
            'host': 'localhost',
            'port': 6379,
            'db_sessions': 5,
            'db_notifications': 11,
            'max_connections': 2 ** 31,
            },
            'cookies': {
            'expires_days': 30,  # 设置过期时间
            'max_age': 20,
            },
        },
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()