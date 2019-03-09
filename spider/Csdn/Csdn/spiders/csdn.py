# -*- coding: utf-8 -*-
import scrapy
from Csdn.items import CsdnItem

class CsdnSpider(scrapy.Spider):
    #爬虫名
    name = 'csdn'
    #爬虫作用范围
    allowed_domains = ['blog.csdn.net']
    #起始url
    start_urls = ['https://blog.csdn.net/qq_24726509/article/details/83958738']
     
    #response为访问start_urls后得到的响应
    def parse(self, response):
        item = CsdnItem()
        # respone.xptah('//h1')结果为选择器对象
        # 结果:[<selector ... data=<h1 class="".>]
        # response.xpath('//h1/text()')结果选择器对象
        # 结果:[<selector ... data="tensflow"]
        # response.xpath('//h1/text()').extract()
        # 结果:["tensflow"]
        
        #标题 选择器对象
        item['title'] = response.xpath('//h1[@class="title-article"]/text()').extract()[0]
        #时间
        item['time'] = response.xpath('//span[@class="time"]/text()').extract()[0]
        #数量
        item['number'] = response.xpath('//span[@class="read-count"]/text()').extract()[0]
        #生成器
        yield item
