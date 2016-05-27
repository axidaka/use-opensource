# -*- coding: utf-8 -*-

__author__ = "zhqs"

# Define here the models for your Spider
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider
import re
import urlparse
import os, sys, copy

reload(sys)
sys.setdefaultencoding("utf-8")

import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import PicItem

#定义全局
pic_save_rootdir = r'G:\运行结果\bizhi'
g_param_picitem = r'picitem'

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

    def transfer_picitem(self, request, picitem):
        """
        通过 request.meta 来传递callback之间的参数
        """
        request.meta[g_param_picitem] = picitem

    def check_picitem(self, response, request):
        """
        将相应中的参数继续传递
        """
        if g_param_picitem in response.meta:
            self.transfer_picitem(request, response.meta[g_param_picitem])

    def get_picitem(self, response):
        if g_param_picitem in response.meta:
            return response.meta[g_param_picitem]
        else:
            None

    def parse(self, response):

        # <a class="all sel"> 壁纸分类
        for selitem in response.xpath("//dl[@class='filter-item first clearfix']//a"):

                # 筛选出带 href, 主要是获取分类的中文名称， 这里的xpath需要使用相对路劲 . 不能省略
                hrefsel = selitem.xpath('./@href')
                if len(hrefsel.extract()) != 0:

                    picitem = PicItem()
                    #text 获取中文分类名称
                    picitem['selection']         = selitem.xpath('./text()').extract()[0]
                    #href 获取地址相对路径
                    picitem['pic_relativepath']  = hrefsel.extract()[0]

                    # 继续请求的分类链接
                    selitem_link = self.dom + hrefsel.extract()[0]
                    request = scrapy.Request(selitem_link, callback=self.parse_selection_item)

                    # 通过meta 传递参数
                    self.transfer_picitem(request, picitem)

                    yield  request

    def parse_selection_item(self, response):

        #/html/body/div[5]/div[1]/ul[1]/li[1]/a 壁纸列表
        for divitem in response.xpath("//li[@class='photo-list-padding']/a[@class='pic']"):

            # 这里需要重新构造参数, 要不然id()返回都是同一个参数对象
            tempPicItem = copy.deepcopy(self.get_picitem(response))

            if tempPicItem is not None:

                href = divitem.xpath('./@href')
                if len(href.extract()) != 0:

                    divitem_link = self.dom + href.extract()[0]
                    request = scrapy.Request(divitem_link, callback=self.parese_divitem)

                    #壁纸列表标题
                    tempPicItem['title'] = divitem.xpath('.//@title').extract()[0]
                    self.transfer_picitem(request, tempPicItem)

                    yield  request

    def parese_divitem(self, response):
        """
        解析 壁纸列表每一项
        """

        #//*[@id="showImg"]/li[1]/a/img
        for groupitem in response.xpath("//ul[@id='showImg']/li/a/@href").extract():
            groupitem_link = self.dom + groupitem
            request = scrapy.Request(groupitem_link, callback=self.parse_detail_item)

            # 检查参数并继续传递
            self.check_picitem(response, request)

            yield  request

    def parse_detail_item(self, response):
        """
        解析 壁纸详情页
        """
        # //*[@id="1920x1080"]
        target = response.xpath("//dd[@id='tagfbl']/a[@id='1920x1080']/@href")
        if target:
            detail_link = self.dom + target[0].extract()
            request = scrapy.Request(detail_link, callback=self.parse_finally)

            # 检查参数并继续传递
            self.check_picitem(response, request)

            yield  request
        else:
            print "Error Canot find 1920x1080"

    def parse_finally(self, response):

        target = response.xpath('//img/@src')
        if target:
            tmpPicItem = self.get_picitem(response)
            if tmpPicItem is not None:
                tmpPicItem['link']    = target.extract()[0]
                tmpPicItem['pic_dom'] = self.allowed_domains[0]
                return  tmpPicItem

        # tmpPicItem = self.get_picitem(response)
        # if  tmpPicItem is not None:
        #     img_itemloader = ItemLoader(item = tmpPicItem, response = response)
        #     img_itemloader.add_xpath('link', '//img/@src')
        #     img_itemloader.add_value('pic_dom', self.allowed_domains[0])
        #     return  img_itemloader.load_item()