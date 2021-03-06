# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link  = scrapy.Field()
    desc  = scrapy.Field()


class PicItem(scrapy.Item):
    """
    用于保存爬图的信息, 主要是链接
    """
    selection        = scrapy.Field()    #分类
    title            = scrapy.Field()    #列表名称
    link             = scrapy.Field()
    pic_relativepath = scrapy.Field()   # 根据层级关系确定保存路劲
    pic_dom          = scrapy.Field()   # 根域名
