# CTRL+Y  删除一行
# CTRL+D  复制一行

# tornado 演示利用自己封装的dbutil工具类操作数据库
# ALT+ENTER
import hashlib
import random
import pymysql
import time

import tornado
from os.path import join, dirname
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_config_file
from tornado.web import Application, RequestHandler, UIModule
#代码向上移动ALT+SHIFT+方向
from day04.util.dbutil import DBUtil
from day04.util.myutils import mymd5


# 用来响应用户请求
# 定义一个类　　继承RequestHandler类

class IndexHandler(RequestHandler):
    # 定义一个方法　重写父类两个方法
    def initialize(self):
        print('initialize方法执行')

    # 响应以get方式发起的请求
    def get(self, *args, **kwargs):
        # 服务器给浏览器的响应内容
        print('get方法执行')
        self.render('login.html')

    # 响应以post方式发起的请求
    def post(self, *args, **kwargs):
        pass

    def on_finish(self):
        print('on_finish方法执行')


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        name = self.get_body_argument('uname', None)
        password = self.get_body_argument('upwd', None)

        dbutil =DBUtil()

        if dbutil.isloginsuccess(name,password):
            self.redirect('/blog')
        else:
            self.redirect('/?msg=fail')


class BlogHandler(RequestHandler):
    # def my_rand(self,a,b):
    #     return random.randint(a,b)

    def get(self, *args, **kwargs):
        # 变量的使用
        # self.render('blog.html',p1=150,p2=250)
        self.render('blog.html')
        # myrand=self.my_rand,
        # blogs=[
        #     {'title':'我的第一篇博客',
        #      'tag':['情感','男女','星座'],
        #      'content':'好长好长的正文',
        #      'author':'某某人',
        #      'avatar':'a.jpg',
        #      'comment':45 },
        #     {'title': '我的第二篇博客',
        #      'tag': ['技术', 'python'],
        #      'content': '学好python',
        #      'author': 'Redhatlxs',
        #      'avatar': None,
        #      'comment': 0}
        # ]

    def post(self, *args, **kwargs):
        pass


# 渲染模板中的类

class MyModule(UIModule):
    # 重写抽象方法,返回必须是字符串
    def render(self, *args, **kwargs):
        msg = ''
        uri = self.request.uri
        # print('uri--->',uri)
        query = self.request.query
        print('query-->', query)
        if query:
            msg = '用户名或密码错误!'

        return self.render_string('module/module_login.html', result=msg)


class MyModuleBlog(UIModule):
    def my_rand(self, a, b):
        return random.randint(a, b)

    def render(self, *args, **kwargs):
        return self.render_string('module/module_blog.html',
                                  myrand=self.my_rand,
                                  blogs=[
                                      {'title': '我的第一篇博客',
                                       'tag': ['情感', '男女', '星座'],
                                       'content': '好长好长的正文',
                                       'author': '某某人',
                                       'avatar': 'a.jpg',
                                       'comment': 45},
                                      {'title': '我的第二篇博客',
                                       'tag': ['技术', 'python'],
                                       'content': '学好python',
                                       'author': 'Redhatlxs',
                                       'avatar': None,
                                       'comment': 0}
                                  ])


class RegisterHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('register.html')

    def post(self, *args, **kwargs):
        # 收集用户提交的注册信息并写入数据库,完成新用户注册
        name = self.get_body_argument('uname', None)
        password = self.get_body_argument('upwd', None)
        city = self.get_body_argument('city', None)

        if name and password and city:
            # 用户头像文件保存在服务器磁盘上对应文件的名称
            avatar_name = None
            # 用户有没有上传头像--request.files.get('')
            files = self.request.files
            avatar = files.get('avatar', None)

            if avatar:
                # 用户上传了头像文件
                # 将用户上传的头像文件保存
                avatar_file = avatar[0]  # 上传的文件内容
                filename = avatar_file.get('filename')
                body = avatar_file.get('body')

                filename = str(time.time()) + filename
                writer = open('mystatics/images/%s' % filename, 'wb')
                writer.write(body)
                writer.close()
                # 将保存文件的名称赋值给avatar_name
                avatar_name = filename

            dbutil = DBUtil()
            print(dbutil)
            try:
                # 执行新增操作时,有可能出现用户名重复的情况,
                # 导致数据库抛出异常
                # 关键字传参数
                # dbutil.registUser(name,password,city,avatar_name)
                params =dict(name=name,password=password,city=city,avatar_name=avatar_name)
                dbutil.registUser(**params)


                self.redirect('/')

            except Exception as e:
                # 打印异常信息
                print('用户名重复',e)
                errmsg=e.__str__()
                print('afas',errmsg)
                self.redirect('/register?msg=%s'%errmsg)

        else:
            self.redirect('/register?msg=fail')


class MyModuleRegist(UIModule):
    def render(self, *args, **kwargs):
        msg = ''
        q = self.request.query
        if q:
            # 有问题msg=fail msg=1062(数据据库内部存在报错)
            # msg='服务器繁忙,稍后重试！'
            info =q.split("=")[1]
            print(info)
            if info=='fail':
                msg = '注册信息不完整！'
            else:
                msg=info
        return self.render_string('module/module_regist.html', result=msg)


# １函数－定义一个变量,用来代表端口号
define('port', type=int, default=8888, multiple=False)

# 定义一个变量,用来代表数据库的连接信息(用户名,密码,端口号,数据库名称)
define('db', multiple=True, type=str, default=[])

# ３从指定的配置文件中,读取port的内容相对路径
parse_config_file('config')

# 创建Application对象,进行若干个对服务器的设置
# 例如：路由类表,模板路径,静态资源路径
# app = Application([('/', IndexHandler)],template_path='mytemplate')
app = Application([('/', IndexHandler), ('/login', LoginHandler),
                   ('/blog', BlogHandler), ('/register', RegisterHandler)],
                  template_path=join(dirname(__file__), 'mytemplate'),
                  static_path=join(dirname(__file__), 'mystatics'),
                  ui_modules={'mymodule': MyModule, 'myblogmodule': MyModuleBlog,
                              'registmodule': MyModuleRegist})
# 创建一个服务器程序
server = HTTPServer(app)
# 服务器监听某个端口(建议使用10000以上的端口)
server.listen(options.port)  # 10000

# 打印获得的数据库参数
print('数据库参数:', options.db)

# 启动服务器(在当前进程中启动服务器)
IOLoop.current().start()




# 先定义变量
# 变量值从配置文件来
# 设置配置文件
# 使用变量


# 全局变量- 配置文件
# 定义－读取－使用


# RequestHandler中方法执行顺序　initialize-get-post-on_finish-finish(系统自带不能改)


#
# 模板步骤：
# 1,写模板
# 2.告诉tornado模板存放哪里
# 3.将模板文件回推到客户端(模板的渲染)


# get 方法中－－－－url地址不能为中文要转为utf8编码
# utf转码或用英文
