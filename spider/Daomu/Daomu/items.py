
import scrapy


class DaomuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #书的名称
    bookName = scrapy.Field()
    #书的标题
    bookTitle = scrapy.Field()
    #章节数量
    zhNum = scrapy.Field()
    #章节名称
    zhName = scrapy.Field()
    #章节链接
    zhLink = scrapy.Field()
