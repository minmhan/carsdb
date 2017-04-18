# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst

class CarsdbItem(Item):
    # define the fields for your item here like:
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    desc = scrapy.Field(output_processor=TakeFirst())
    submitted = scrapy.Field(output_processor=TakeFirst())
    fuel = scrapy.Field(output_processor=TakeFirst())
    engine_power = scrapy.Field(output_processor=TakeFirst())
    dealer = scrapy.Field(output_processor=TakeFirst())

    
    #House keeping field
    url = Field(output_processor=TakeFirst())
    project = Field(output_processor=TakeFirst())
    spider = Field(output_processor=TakeFirst())
    server = Field(output_processor=TakeFirst())
    date = Field(output_processor=TakeFirst())
