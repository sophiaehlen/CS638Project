# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field



class CraigslistItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = Field()
    title = Field()
    attr = Field()
    price = Field()
    postbody = Field()
    location = Field()
    postdate = Field()

    vin = Field()
    odometer = Field()
    condition = Field()
    cylinders = Field()
    drive = Field()
    fuel = Field()
    paint_color = Field()
    size = Field()
    title_status = Field()
