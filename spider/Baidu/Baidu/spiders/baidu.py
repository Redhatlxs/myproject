# -*- coding: utf-8 -*-
import scrapy


class BaiduSpider(scrapy.Spider):
    #爬虫名,运行爬虫时的名字
    name = 'baidu'
    #允许爬取的域名
    allowed_domains = ['www.baidu.com']
    #开始要爬取的URL
    start_urls = ['http://www.baidu.com/']
    
    #parse函数名不能改
    def parse(self, response):
        with open("百度.html","w")as f:
            f.write(response.text)
