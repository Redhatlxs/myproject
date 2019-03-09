import requests
import re
import pymongo

class lianjiaSpider:
    def __init__(self):
        self.baseurl="https://jn.lianjia.com/ershoufang/"
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.proxies= {"http":"http://61.142.72.154:50924"}
        self.page=1

      #连接对象
        self.conn = pymongo.MongoClient("localhost",27017)
      #数据库对象
        self.db = self.conn['lianjia']
        #集合对象
        self.myset = self.db['house']




        

    def getPage(self,url):

       res =requests.get(url,self.proxies,headers=self.headers)
       res.enconding = "utf-8"
       html = res.text
       self.parsePage(html)


 

    def parsePage(self,html):
       
       p = re.compile('<div class="houseInfo">.*?data-el="region">(.*?)</a>.*?<div class="totalPrice">.*?<span>(.*?)</span>',re.S)  
       r_list = p.findall(html)
       self.writeTomongo(r_list)
     

    def writeTomongo(self,r_list):
        for r in r_list:
          D ={
              "name":r[0].strip(),
              "price":float(r[1].strip())*10000
          }
          self.myset.insert(D)
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