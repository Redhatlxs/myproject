# CTRL+Y  删除一行
# CTRL+D  复制一行

# tornado 演示 通过继承Application类添加自定义属性
#每次使用dbutil操作数据表时,不用反复构建对象

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
from day04.myapp.myapplication import MyApplication
from day04.myconfig import myconfig
from day04.myhandlers.myhandlers import IndexHandler, LoginHandler, BlogHandler, RegisterHandler, CheckHandler
from day04.mymodulers.mymodulers import MyModule, MyModuleBlog, MyModuleRegist
from day04.util.dbutil import DBUtil
from day04.util.myutils import mymd5





# 创建Application对象,进行若干个对服务器的设置
# 例如：路由类表,模板路径,静态资源路径
# app = Application([('/', IndexHandler)],template_path='mytemplate')
app = MyApplication([('/', IndexHandler), ('/login', LoginHandler),
                   ('/blog', BlogHandler), ('/register', RegisterHandler),('/check',CheckHandler)],
                  tp=join(dirname(__file__), 'mytemplate'),
                  sp=join(dirname(__file__), 'mystatics'),
                  um={'mymodule': MyModule, 'myblogmodule': MyModuleBlog,
                              'registmodule': MyModuleRegist})
# 创建一个服务器程序
server = HTTPServer(app)
# 服务器监听某个端口(建议使用10000以上的端口)
server.listen(myconfig.configs['port'])  # 10000

# 启动服务器(在当前进程中启动服务器)
IOLoop.current().start()




# 先定义变量
# 变量值从配置文件来
# 设置配置文件
# 使用变量


# 全局变量- 配置文件
# 定义－读取－使用


# RequestHandler中方法执行顺序initialize-get-post-on_finish-finish(系统自带不能改)


#
# 模板步骤：
# 1,写模板
# 2.告诉tornado模板存放哪里
# 3.将模板文件回推到客户端(模板的渲染)


# get 方法中－－－－url地址不能为中文要转为utf8编码
# utf转码或用英文
