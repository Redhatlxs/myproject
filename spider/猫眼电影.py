# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 11:53:11 2018

@author: Python
"""

import pymongo
import urllib.request
import re

#with open("test.csv","a",newline="") as f:
#    
#    #初始化写入对象
#    writer = csv.writer(f)
#    #写入对象的writerow方法
#    writer.writerow(['霸王别姬','张国荣',"1993"])
#    writer.writerow(['英雄','梁朝伟',"2000"])
#    writer.writerow(['蜘蛛侠','小白','2003'])
#    
    
class MaoyanSpider:
   def __init__(self):
        self.headers ={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.baseurl= "http://maoyan.com/board/4?offset="
        self.offset =0
        self.page=1
      #连接对象
        self.conn = pymongo.MongoClient("localhost",27017)
      #数据库对象
        self.db = self.conn.myfilm
        #集合对象
        self.tab = self.db.top100


        
   #得到网页
   def getPage(self,url):
        req=urllib.request.Request(url,headers=self.headers)
        res=urllib.request.urlopen(req)
        html=res.read().decode("utf-8")
        self.parsePage(html)
        
    #解析网页
   def parsePage(self,html):
        p = re.compile('<div class="movie-item-info">.*?title="(.*?)".*?class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>',re.S)
        r_list =p.findall(html)
        self.writeTomongo(r_list)       
        
   #保存数据
   def writeTomongo(self,r_list):
       for r_tuple in r_list:
          name = r_tuple[0].strip()
          star = r_tuple[1].strip()
          time = r_tuple[2].strip()

          d = {"name":name,"star":star,"time":time}

       self.tab.insert(d)
       print("存入数据库成功")

      
          
   
    #主函数
   def workOn(self):
       while True:
           c = input("爬按y,退出按q:")
           if c.strip().lower()=="y":          
               url =self.baseurl+str(self.offset)
               self.getPage(url)
               self.page +=1
               self.offset=(self.page-1)*10
           else:
              print("爬取结束")
              break
       
   
    
if __name__=="__main__":
    spider = MaoyanSpider()
    spider.workOn()    
     


    

    
    
    
    
#    
#<div class="movie-item-info">.*?title=(.*?).*?class="star">(.*?)</p>
#.*?class="releasetime">(.*?)</p>  
    
    

