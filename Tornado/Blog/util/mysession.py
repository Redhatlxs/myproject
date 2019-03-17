from day04.util.myutils import myuuid

#MySession用来存储客户端信息
#存储格式:
#键 id
#值 {}
#12312451231:{'islogin':'True','yyy':'yyy'}
#1568748484e:{'aaa':'bbb','ccc':'ddd'}


session={}

# 模拟实现session机制
class MySession:
    def __init__(self,handler):
        self.handler=handler


# 取信息
    def __getitem__(self, key):
        # x = li[0]
        # x = li.__getitem__(0)
        # y = my['key']
        # y = my.__getitem__('key')
        id = self.handler.get_cookie('cookieid')
        if id:
            #根据id取出对应的存储在服务器上的信息
            info = session.get(id,None)
            if info:
                return info.get(key,None)
            else:
                return None
        else:
            return None

# 写信息
    def __setitem__(self, key, value):
        # li[0]=1
        # li.__setitem__(0,1)
        # mydict['key']='value1'
        # mydict.__setitem__('key','value1')
        id = self.handler.get_cookie('cokieid')
        if id:
            info =session.get(id,None)
            if info:
                info[key]=value
            else:
                d=dict()
                d[key]=value
                session[id]=d
        else:
            d= dict()
            d[key]=value
            #为客户端指定一个uuid充当id值
            id =myuuid()
            session[id] = d
            #并将id以cookie的形式写回给浏览器
            self.handler.set_cookie('cookieid',id,expires_days=10)












