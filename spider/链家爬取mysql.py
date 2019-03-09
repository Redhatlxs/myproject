import requests
import re
import pymysql

class lianjiaSpider:
    def __init__(self):
        self.baseurl="https://jn.lianjia.com/ershoufang/"
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.proxies= {"http":"http://61.142.72.154:50924"}
        self.db = pymysql.connect("localhost","root","123456","lianjia",charset="utf8")
        self.cursor = self.db.cursor()
        self.page=1
        

    def getPage(self,url):

       res =requests.get(url,self.proxies,headers=self.headers)
       res.enconding = "utf-8"
       html = res.text
       self.parsePage(html)


 

    def parsePage(self,html):
       
       p = re.compile('<div class="houseInfo">.*?data-el="region">(.*?)</a>.*?<div class="totalPrice">.*?<span>(.*?)</span>',re.S)  
       r_list = p.findall(html)
       self.writeTomysql(r_list)
     

    def writeTomysql(self,r_list):
       ins = 'insert into house(name,price)\
       values(%s,%s)'
       for r in r_list:
           L=[r[0].strip(),
              float(r[1].strip())*10000]
           self.cursor.execute(ins,L)   
           self.db.commit()
           print("存入数据成功")


    def workOn(self):
        self.getPage(self.baseurl)
        while True:
            c = input("爬按y,退出按q:")
            if c == "y":
                self.page +=1
                url = self.baseurl +"pg"+str(self.page)+"/"
                self.getPage(url)
            else:
                print("爬去结束")
                break



    
if __name__=="__main__":
    spider = lianjiaSpider()
    spider.workOn()  