# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import  os
import urllib, urllib2

import settings

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class PicDownloadPipeline(object):

    def process_item(self, item, spider):

        if 'selection' in item and 'link' in item and 'pic_relativepath' in item and 'pic_dom' in item:
            pic_resolution = item['pic_relativepath'].split('/')[2]
            pic_savepath = os.path.join(settings.IMAGES_STORE, item['pic_dom'], item['selection'], pic_resolution,
                                        item['title'])
            if not os.path.exists(pic_savepath):
                os.makedirs(pic_savepath)

            link = item['link']
            jpgname = os.path.basename(link)
            pic_savepath = os.path.join(pic_savepath, jpgname)
            if os.path.exists(pic_savepath):
                return

            try:
                urllib2.urlopen(link)
                urllib.urlretrieve(link, pic_savepath)
                print 'picpath', pic_savepath
            except urllib2.HTTPError, e:
                pass

    # def get_media_requests(self, item, info):
    #     if 'link' in item:
    #         print 'link', item['link']
    #         yield scrapy.Request(item['link'])
    #
    # def item_completed(self, results, item, info):
    #     image_paths = [x['path'] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem("Item contains no images")
    #     print 'completed:', image_paths
    #
    #     if 'selection' in item and 'link' in item and 'pic_relativepath' in item and 'pic_dom' in item:
    #         pic_resolution = item['pic_relativepath'].split('/')[2]
    #         pic_savepath = os.path.join(item['pic_dom'], item['selection'], pic_resolution,
    #                                     item['title'])
    #         # if not os.path.exists(pic_savepath):
    #         #     os.makedirs(pic_savepath)
    #
    #         jpgname = os.path.basename(item['link'])
    #         pic_savepath = os.path.join(pic_savepath, jpgname)
    #
    #         item['image_paths'] = pic_savepath
    #         return item

    # def file_path(self, request, response=None, info=None):
    #     item = response.meta["picitem"]
    #
    #     if 'selection' in item and 'link' in item and 'pic_relativepath' in item and 'pic_dom' in item:
    #         pic_resolution = item['pic_relativepath'].split('/')[2]
    #         pic_savepath = os.path.join(item['pic_dom'], item['selection'], pic_resolution,
    #                                     item['title'])
    #         # if not os.path.exists(pic_savepath):
    #         #     os.makedirs(pic_savepath)
    #
    #         jpgname = os.path.basename(item['link'])
    #         pic_savepath = os.path.join(pic_savepath, jpgname)
    #
    #         print 'last:', pic_savepath
    #
    #         return pic_savepath

    # def process_item(self, item, spider):
    #     if 'selection' in item and 'link' in item and 'pic_relativepath' in item and 'pic_dom' in item:
    #         pic_resolution = item['pic_relativepath'].split('/')[2]
    #         pic_savepath = os.path.join(settings.IMAGES_STORE, item['pic_dom'], item['selection'], pic_resolution, item['title'])
    #         if not os.path.exists(pic_savepath):
    #             os.makedirs(pic_savepath)
    #
    #         jpgname = os.path.basename(item['link'])
    #         pic_savepath = os.path.join(pic_savepath, jpgname)
    #
    #         with open(pic_savepath, 'wb') as fileoobj:
    #             response =