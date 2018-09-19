# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EngNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    pubtime = scrapy.Field()
    topic = scrapy.Field()
#    comment_num = scrapy.Field()
#    share_num = scrapy.Field()
    main_text = scrapy.Field()
    
    pass