# -*- coding: utf-8 -*-
import re
import logging
import scrapy
from scrapy.http import FormRequest
from patents.items import InfoItem


class PatentsSpider(scrapy.Spider):
    logger = None
    name = "patents_spider"
    allowed_domains = ["www.pss-system.gov.cn"]
    company_list = [
        u'卡斯柯信号有限公司',
        u'北京全路通信信号研究设计院',
        u'北京全路通信信号研究设计院集团有限公司',
        u'北京全路通信信号研究设计院有限公司',
        u'上海富欣智能交通控制有限公司',
        u'北京交控科技股份有限公司',
        u'北京和利时系统工程有限公司',
        u'中国铁道科学研究院通信信号研究所',
        u'南京恩瑞特实业有限公司',
        u'北京交大微联科技有限公司',
        u'浙江众合科技股份有限公司',
        u'浙江众合机电股份有限公司',
        u'上海亨钧科技股份有限公司',
    ]

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def start_requests(self):
        url = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/general_smartSearch-executeSmartSearch.shtml'
        data = {
            'searchCondition.searchExp': '',
            'search_scope:': '',
            'searchCondition.dbId': 'VDB',
            'resultPagination.limit': '12',
            'searchCondition.searchType': 'Sino_foreign',
            'wee.bizlog.modulelevel': '0200101'

        }
        for company in self.company_list:
            data['searchCondition.searchExp'] = company
            yield FormRequest(url=url, formdata=data, callback=self.parse_first_page, dont_filter=True, meta={'company':company, 'dont_redirect': True})

    def parse_first_page(self, response):
        company = response.meta.get('company', '')
        text = response.xpath(("//div[@class='page_top']")).extract_first()
        try:
            text = re.findall(u'共.*条数据', text)[0]
            nums = re.findall(u'(\d+)', text)
            if int(nums[0]) <= (nums[1]):
                max_page = int(nums[0])
                total = int(nums[1])
            else:
                max_page = int(nums[1])
                total = int(nums[0])
            self.logger.info(u'[{0}]: get first page success. {1} '.format(company, text))
            self.logger.debug(u'[{0}]: max page: {1}, total: {2}'.format(company, max_page, total))
        except Exception as e:
            self.logger.error(e)
            self.logger.info(u'[{0}]: parse first page failed. response code: {1}, content: {2}. request url: {3}'.format(company, response.status, response.text, response.url))
            return
