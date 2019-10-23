# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MiamidadeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	FolioNumber = scrapy.Field()
	Address = scrapy.Field()
	Owner = scrapy.Field()
	Sale_Type = scrapy.Field()
	MailingAddress = scrapy.Field()
	Sale_Date = scrapy.Field()
	Sale_Price = scrapy.Field()
	MStreet = scrapy.Field()
	AStreet = scrapy.Field()
	MCity = scrapy.Field()
	ACity = scrapy.Field()
	MState = scrapy.Field()
	AState = scrapy.Field()
	MZipcode = scrapy.Field()
	AZipcode = scrapy.Field()

	pass
