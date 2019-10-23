# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BcpaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    website = scrapy.Field()
    property_owner = scrapy.Field()
    mail = scrapy.Field()
    sid = scrapy.Field()
    Saled_Date = scrapy.Field()
    Saled_Price = scrapy.Field()
    Saled_Type = scrapy.Field()
    url = scrapy.Field()
    street = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()
    pass
