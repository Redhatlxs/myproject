# util 封装
import hashlib
from uuid import uuid4


def mymd5(orginal):

    md = hashlib.md5()
    md.update(orginal.encode('utf8'))
    m= md.hexdigest()
    return m

#生成uuid字符串
# 通用唯一识别码
def myuuid():
    u = uuid4()
    # 转成二进制格式u.bytes
    print('afafda',u.bytes)
    md =hashlib.md5()
    md.update(u.bytes)
    m= md.hexdigest()
    return m




