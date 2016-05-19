# -*- coding: utf-8 -*-

__author__ = "zhqs"

# Define here the models for your Spider
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider

import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"];
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        print '调试输出', response.url
        filename = response.url.split("/")[-2] + '.html';
        with open(filename, "wb") as f:
            f.write(response.body)