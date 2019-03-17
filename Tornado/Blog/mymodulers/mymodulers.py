# 渲染模板中的类
import random

from tornado.web import UIModule


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
