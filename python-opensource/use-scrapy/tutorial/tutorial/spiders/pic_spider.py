# -*- coding: utf-8 -*-

__author__ = "zhqs"

# Define here the models for your Spider
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider
import re
import urlparse
import os, sys

reload(sys)
sys.setdefaultencoding("utf-8")

import scrapy
from tutorial.items import PicItem

#定义全局
pic_save_rootdir = r'G:\运行结果\bizhi'

class PicSpider(scrapy.Spider):
    """
    爬网络图片
    """
    name = "picspider"
    allowed_domains = ["desk.zol.com.cn"];
    start_urls = [
        "http://desk.zol.com.cn/1920x1080/",
    ]

    def __init__(self):
        self.dom = "http://desk.zol.com.cn"

    def parse(self, response):
        print 'HomePage>>:', type(response).__name__, response.url

        # <a class="all sel"> 壁纸分类
        for selitem in response.xpath("//dl[@class='filter-item first clearfix']//a/@href").extract():
            selitem_link = self.dom + selitem
            request = scrapy.Request(selitem_link, callback=self.parse_selection_item)
            yield  request

    def parse_selection_item(self, response):
        print '     SelItem>>:', type(response).__name__, response.url
        #/html/body/div[5]/div[1]/ul[1]/li[1]/a 壁纸列表
        for divitem in response.xpath("//li[@class='photo-list-padding']/a[@class='pic']/@href").extract():
            divitem_link = self.dom + divitem
            request = scrapy.Request(divitem_link, callback=self.parese_divitem)
            yield  request

    def parese_divitem(self, response):
        """
        解析 壁纸列表每一项
        """
        print '         divitem>>:', type(response).__name__, response.url

        #//*[@id="showImg"]/li[1]/a/img
        for groupitem in response.xpath("//ul[@id='showImg']/li/a/@href").extract():
            groupitem_link = self.dom + groupitem
            request = scrapy.Request(groupitem_link, callback=self.parse_detail_item)
            yield  request

    def parse_detail_item(self, response):
        """
        解析 壁纸详情页
        """
        # //*[@id="1920x1080"]
        print '             detailitem>>:', type(response).__name__, response.url
        target = response.xpath("//dd[@id='tagfbl']/a[@id='1920x1080']/@href")
        if target:
            detail_link = self.dom + target[0].extract()
            yield  scrapy.Request(detail_link, callback=self.parse_finally)
        else:
            print "Error Canot find 1920x1080"

    def parse_finally(self, response):
        print '                 finally>>:', type(response).__name__, response.url
        target = response.xpath('//img/@src')
        if target:
            img_item = PicItem()
            img_item['link'] = target[0].extract()
            yield  img_item