# 数据库封装
import pymysql

from day04.util.myutils import mymd5


class DBUtil:
    def __init__(self,**kwargs):
        #获取到与数据库的连接

        #直接使用用户传递的内容不太好
        #应该简单的提取
        host = kwargs.get('host','127.0.0.1')
        port = kwargs.get('port',3306)
        user = kwargs.get('user','root')
        password = kwargs.get('password','123456')
        database = kwargs.get('database','blogdb')
        charset = kwargs.get('charset','utf8')
       #把经过提取的内容作为参数传递给connect方法
        configs=dict(host=host,port=port,user=user,password=password,
                     database=database,charset=charset)
        conn = pymysql.connect(**configs)
        # 进而获取结果集
        if conn:
            self.cursor=conn.cursor()
        else:
            raise Exception('数据库连接参数错误！')



    # 注册用户－－ 关键字传参组织成字典＊＊kwargs
    def registUser(self,**kwargs):
        name=kwargs.get('name')
        password = kwargs.get('password')
        pwd = mymd5(password)
        city = kwargs.get('city')
        avatar_name = kwargs.get('avatar_name')
    # def registUser(self,name,password,city,avatar_name):

        sql='insert into tb_user(user_name, user_password,user_city,user_avatar)values(%s,%s,%s,%s)'

        params=(name,pwd,city,avatar_name)
        try:
            self.cursor.execute(sql,params)
            self.cursor.connection.commit()

        except Exception as e:
            # info = e.__str__()---->(1062, "Duplicate entry 'abc' for key 'user_name'")
            # raise Exception(e.__str__())#设计者考虑用户
            info = e.__str__()
            m = info.split(',')[0]
            # # errmsg = m[1:]
            errmsg = m.split('(')[1]
            err='数据库未知错误!'
            if errmsg=='1062':
                err = '用户名重复'
            raise Exception(err)


    #登录
    # 根据参数中提供的用户名和密码
    # 取数据库tb_user表中查询是否有匹配的数据记录
    # 如果有,就返回True,否则False
    def isloginsuccess(self,name,password):

        sql= 'select count(*) from tb_user where user_name=%s and user_password=%s'

        pwd = mymd5(password)
        params =(name,pwd)

        self.cursor.execute(sql,params)
        result = self.cursor.fetchone()

        if result[0]:
            return True
        else:
            return False


    #判断某个用户是否存在
    def hasUser(self,username):
        #利用username去tb_user表查询
        #retrun True/False
        sql='select count(*) from tb_user where user_name=%s'
        # 元组
        params=(username,)
        self.cursor.execute(sql,params)
        result = self.cursor.fetchone()
        #True 该用户名已经存在
        #False 该用户名不存在
        if result[0]:
            return True
        else:
            return False
        
    def findAvatar(self,username):
        sql = 'select user_avatar from tb_user where user_name=%s'
        params=(username,)
        self.cursor.execute(sql,params)
        result = self.cursor.fetchone()
        # print('我的',result)
        if result[0]:
            return result[0]
        else:
            return None

        

