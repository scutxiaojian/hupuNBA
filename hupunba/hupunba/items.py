# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HupunbaItem(scrapy.Item):
    # define the fields for your item here like:
    rank = scrapy.Field()
    name = scrapy.Field()
    team = scrapy.Field()
    point = scrapy.Field()
    fgs = scrapy.Field()
    threefgs = scrapy.Field()
    freethrowfgs = scrapy.Field()
    matchnumber = scrapy.Field()
    time = scrapy.Field()
