# auth =("用户名","密码")
# auth=("tarenacode","code_2013")
# 正则表达式：<a href=".*?">(.*?)</a>
# Web客户端验证

import requests
import re
import pymysql
import warnings

class DaneiSpider:
    def __init__(self):
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.proxies= {"http":"http://61.142.72.154:50924"}
        self.url= "http://code.tarena.com.cn/"
        #连接对象
        self.db = pymysql.connect("localhost","root","123456","lianjia",charset="utf8")
        #游标对象
        self.cursor =self.db.cursor()
      
    def getParse(self,url):
        res = requests.get(url,self.proxies,headers=self.headers,auth=("tarenacode","code_2013"))
        res.encoding ="utf-8"
        # 页面获取的内容
        html = res.text
        # 正则匹配
        p= re.compile('<a href=".*?">(.*?)</a>',re.S)
        r_list = p.findall(html)
        self.mysql(r_list)

    def mysql(self,r_list):
        ctab = 'create table code(\
               id int primary key auto_increment,\
               course varchar(30)\
               )'
        ins = 'insert into code(course)values(%s)'
        warnings.filterwarnings("ignore")
        try:
            self.cursor.execute(ctab)
        except:
            pass
        for r in r_list:
            L = [r.strip()[0:-1]]
            self.cursor.execute(ins,L)
            self.db.commit()
            print("达内code已入库")

    def workOn(self):
        while True:
            c = input("爬按y,退出按q:")
            if c.strip().lower()=="y":
               url =self.url
               self.getParse(url)
            else:
               print("爬取结束")
               break
            
if __name__=="__main__":
    spider = DaneiSpider()
    spider.workOn() 