# -*- coding: utf-8 -*-
import os
import re
import csv
import logging
import scrapy

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class PatentsSpider(scrapy.Spider):
    logger = None
    name = "patents_spider"
    allowed_domains = ["www.pss-system.gov.cn"]
    company_list = [
        u'卡斯柯信号有限公司',
        # u'北京全路通信信号研究设计院',
        # u'北京全路通信信号研究设计院集团有限公司',
        # u'北京全路通信信号研究设计院有限公司',
        # u'上海富欣智能交通控制有限公司',
        # u'北京交控科技股份有限公司',
        # u'北京和利时系统工程有限公司',
        # u'中国铁道科学研究院通信信号研究所',
        # u'南京恩瑞特实业有限公司',
        # u'北京交大微联科技有限公司',
        # u'浙江众合科技股份有限公司',
        # u'浙江众合机电股份有限公司',
        # u'上海亨钧科技股份有限公司',
    ]

    def __init__(self):
        self.result_path = 'result.csv'
        self.logger = logging.getLogger(__name__)
        self.search_url = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/searchHomeIndex-searchHomeIndex.shtml'

    def start_requests(self):
        for company in self.company_list:
            self.get_app_num_by_company_name(company)

    def get_app_num_by_company_name(self, company):
        ''' 获取公司的所有的专利申请号

        :param company:
        :return:
        '''

        session = webdriver.Chrome()
        session.get(self.search_url)
        inp = session.find_element_by_id('search_input')
        inp.send_keys(company)
        sleep(2)
        inp.send_keys(Keys.ENTER)

        # 进入搜索结构页面
        sleep(2)
        page_source = session.page_source
        sleep(5)
        text = re.findall(u'共.*条数据', page_source)[0]
        nums = re.findall(u'(\d+)', text)
        if int(nums[0]) <= (nums[1]):
            max_page = int(nums[0])
            total = int(nums[1])
        else:
            max_page = int(nums[1])
            total = int(nums[0])
        self.logger.info(u'[{0}]: get first page success. {1} '.format(company, text))
        self.logger.debug(u'[{0}]: max page: {1}, total: {2}'.format(company, max_page, total))

        # 遍历多页得到专利申请号
        for page in xrange(22, max_page + 1):
            try:
                inp = session.find_element_by_id('txt')
                inp.clear()
                inp.send_keys(str(page))
                sleep(2)
                inp.send_keys(Keys.ENTER)
                sleep(2)
                page_source = session.page_source
                sleep(5)
                select = Selector(text=page_source)
                app_nums = select.xpath("//div[@class='item-content-body left']/p[1]/text()").extract()
                self.logger.info('crawl page: {} success.'.format(page))
            except:
                self.logger.info('crawl page: {} failed.'.format(page))
                continue

            file_exists = os.path.isfile(self.result_path)
            with open(self.result_path, 'a') as f:
                fieldnames = [u'发明名称', u'申请号', u'申请日', u'公开号', u'IPC分类号', u'申请人', u'发明人', u'摘要', u'法律状态']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                for num in app_nums:
                    writer.writerow({
                        u'发明名称': '',
                        u'申请号': num,
                        u'申请日': '',
                        u'公开号': '',
                        u'IPC分类号': '',
                        u'申请人': '',
                        u'发明人': '',
                        u'摘要': '',
                        u'法律状态': ''})