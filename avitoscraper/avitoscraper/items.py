# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AvitoscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PropertyItem(scrapy.Item):
    url = scrapy.Field()
    ad_title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    category = scrapy.Field()
    is_new_building = scrapy.Field()
    phone = scrapy.Field()
    published_date = scrapy.Field()
    seller_name = scrapy.Field()
    habitable_size = scrapy.Field()
    total_surface = scrapy.Field()    
