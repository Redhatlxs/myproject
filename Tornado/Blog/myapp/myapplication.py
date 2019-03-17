from tornado.web import Application

# 继承Application
from day04.util.dbutil import DBUtil


class MyApplication(Application):
    def __init__(self,routers,tp,sp,um):
        # 关键字传参
        super().__init__(handlers=routers,template_path=tp,static_path=sp,
                         ui_modules=um)
        self.dbutil =DBUtil()



# 位置传参和关键字传参