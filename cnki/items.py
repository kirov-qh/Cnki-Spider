# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/late st/topics/items.html

from sched import scheduler

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join

class CnkiItem(scrapy.Item):
    'Here define the data structure of spider.'
    title = scrapy.Field()
    abstract = scrapy.Field()
    keyword = scrapy.Field()

