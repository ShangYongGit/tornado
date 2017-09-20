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
        self.current_user = self.session.get('user')
        return self.current_user


# 定义一个请求处理逻辑
class IndexHandler(tornado.web.RequestHandler):
    # @tornado.web.authenticated
    def get(self):
        self.render('temp_index1.html')
        def get(self):
            namelist = ['aaa', 'bbb', 'ccc', 'ddd']
            urllist = [
                ("http://www.baidu.com", u'百度'),
                ("http://www.163.com", u'网易'),
                ("http://www.sina.com", u'新浪'),
            ]
            atag = u'<a href="http://www.baidu.com" target="_blank">---百度---</a><br/>'
            scr = u"<script>alert(document.cookie)</script>"
            self.render(u"temp_index1.html",
                        username=self.current_user,
                        time=time,
                        aa=self.aa,
                        namelist=namelist,
                        urllist=urllist,
                        atag=atag,
                        scr=scr
                        )


class UserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("user登录成功")


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html',nextname = self.get_argument("next", "/"))

    def post(self):
        name = self.get_argument('name','')
        password = self.get_argument('password','')
        if name == 'aaa' and password == '111':
            self.set_secure_cookie("aaa", "bbb")
            self.session.set('user',name)
            self.redirect(self.get_argument("aaa", "/"))
        else:
            self.write('登陆失败！')


# 项目入口
if __name__ == '__main__':
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