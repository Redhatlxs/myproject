# qiushibaike.py
import requests
import pymongo
from lxml import etree

class QishiSpider:
    def __init__(self):
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.conn = pymongo.MongoClient("localhost",27017)
        self.db = self.conn['qiushi']
        self.myset = self.db['qiushiinfo']
      

    def getPage(self,url):
        res = requests.get(url,headers=self.headers)
        res.enconding ="utf-8"
        html = res.text
        self.parsePage(html)


    def parsePage(self,html):
        parseHtml = etree.HTML(html)
        base_list = parseHtml.xpath('//div[contains(@id,"qiushi_tag_")]')
        for base in base_list:
            #节点对象可调用xpath
             #用户昵称
            username = base.xpath('./div/a/h2')
            if len(username) == 0:
                username = "匿名用户"
            else:
                username = username[0].text.strip()



             #段子内容
            content = base.xpath('.//div[@class="content"]/span')
             #好笑数量
            laughNum = base.xpath('.//i')[0]
             #评论数量
            pingNum = base.xpath('.//i')[1]
            d={
                 "username":username,
                 "content":content[0].text,
                 'laughNum':laughNum.text,
                 'pingNum':pingNum.text
                 }
            self.myset.insert(d)
            print("成功")



if __name__ =="__main__":
    spider = QishiSpider()
    spider.getPage("https://www.qiushibaike.com/8hr/page/1/")