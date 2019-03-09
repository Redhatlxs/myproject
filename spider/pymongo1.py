import pymongo
#创建链接对象
conn = pymongo.MongoClient("localhost",27017)
#数据库对象，spiderdb为库名
db = conn.spiderdb
#集合对象，t1是集合名
myset = db.t1
#插入数据
myset.insert({"name":"Lucy"})