# -*- coding: utf-8 -*-

__author__ = "zhqs"

# Define here the models for your Spider
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider
import re

import scrapy
from tutorial.items import TutorialItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"];
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        # print '********MyDebugOutput', response.url
        # filename = response.url.split("/")[-2] + '.html';
        # with open(filename, "wb") as f:
        #     f.write(response.body)

        for sel in response.xpath('//ul/li'):
            item = TutorialItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link']  = sel.xpath('a/@href').extract()
            item['desc']  = sel.xpath('text()').extract()
            yield  item


class DmozSpider_link(scrapy.Spider):

    name = "dmoz-link"
    allowed_domains = ["dmoz.org"];
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/",
    ]

    def parse(self, response):
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            print url
            yield scrapy.Request(url, callback=self.parse_dir_contents)


    def parse_dir_contents(self, response):
        for sel in response.xpath('//ul/li'):
            item = TutorialItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            print item
            yield item




