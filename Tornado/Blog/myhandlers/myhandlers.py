import random

import time
from tornado.web import RequestHandler

from day04.myhandlers.myrequesthandler import MyRequestHandler
from day04.util.mysession import MySession
from day04.util.myutils import myuuid


class IndexHandler(MyRequestHandler):
    # 定义一个方法　重写父类两个方法
    def initialize(self):
        print('initialize方法执行')

    # 响应以get方式发起的请求
    def get(self, *args, **kwargs):
        # 服务器给浏览器的响应内容
        print('get方法执行')

        print('uuid的值--->',myuuid())

        #给浏览器一个cookie
        self.set_cookie('mycookie','helloworld',expires_days=10)

        # session = MySession(self)
        islogin =self.session['islogin']

        if islogin:
            self.redirect('/blog')
        else:
            #服务器给浏览器的响应
            self.render('login.html')


    # 响应以post方式发起的请求
    def post(self, *args, **kwargs):
        pass

    def on_finish(self):
        print('on_finish方法执行')


class LoginHandler(MyRequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        name = self.get_body_argument('uname', None)
        password = self.get_body_argument('upwd', None)

        if self.application.dbutil.isloginsuccess(name,password):

            #登录成功我要在session中记录
            # session=MySession(self)
            self.session['islogin'] = True

            self.redirect('/blog')
        else:
            self.redirect('/?msg=fail')


class BlogHandler(MyRequestHandler):
    def my_rand(self,a,b):
        return random.randint(a,b)

    def get(self, *args, **kwargs):

        # session = MySession(self)
        islogin = self.session['islogin']
        if islogin:
            self.render('blog.html')
        else:
            self.redirect('/')


    def post(self, *args, **kwargs):
        pass

class RegisterHandler(MyRequestHandler):
    def get(self, *args, **kwargs):

        info = self.get_cookie('mycookie')
        print('mycookie的值',info)

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

            try:
                # 执行新增操作时,有可能出现用户名重复的情况,
                # 导致数据库抛出异常
                # 关键字传参数
                # dbutil.registUser(name,password,city,avatar_name)
                params =dict(name=name,password=password,city=city,avatar_name=avatar_name)

                self.application.dbutil.registUser(**params)
                self.redirect('/')

            except Exception as e:
                # 打印异常信息
                print('用户名重复',e)
                errmsg=e.__str__()
                print('afas',errmsg)
                self.redirect('/register?msg=%s'%errmsg)

        else:
            self.redirect('/register?msg=fail')


class CheckHandler(MyRequestHandler):
    def get(self, *args, **kwargs):
        pass
    def post(self, *args, **kwargs):
        #hasuser findavatar
        type =self.get_body_argument('type')

        username = self.get_body_argument('username')
        print('获取到的username:--->',username)

        if type=='hasuser':
        # 利用dbutil去根据username查询
        # tb_user表中是否已有该用户名
            if self.application.dbutil.hasUser(username):
                result = dict(msg='no ok')
            else:
                result = dict(msg='ok')
            self.write(result)

        #查询头像
        if type == 'findavatar':
            avatarname = self.application.dbutil.findAvatar(username)
            # print("hahha",avatarname)
            if avatarname:
                result = dict(msg=avatarname)
            else:
                result = dict(msg="default.jpg")

            self.write(result)





