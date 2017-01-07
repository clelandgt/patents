# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Field, Item


class InfoItem(Item):
    id = Field()
    name = Field()
    app_num = Field()
    app_data = Field()
    pub_num = Field()
    ipc_num = Field()
    app_person = Field()
    inventor = Field()
    intro = Field()
    legal_status = Field()
    url = Field()
    parents_url = Field()
    page_num = Field()



