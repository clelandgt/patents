# -*- coding: utf-8 -*-
import scrapy


class PatentsSpiderSpider(scrapy.Spider):
    name = "patents_spider"
    allowed_domains = ["www.pss-system.gov.cn"]
    start_urls = ['http://www.pss-system.gov.cn/']

    def parse(self, response):
        pass
