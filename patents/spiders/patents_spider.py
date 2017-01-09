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
        self.result_path = 'results.csv'
        self.logger = logging.getLogger(__name__)
        self.search_url = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/searchHomeIndex-searchHomeIndex.shtml'

    def start_requests(self):
        for company in self.company_list:
            # self.get_app_num_by_company_name(company)
            self.crawl_patents()

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
            except Exception as e:
                self.logger.error(e)
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
        session.quit()

    def load_csv(self, path):
        results = []
        with open(path, 'r') as f:
            csv_reader = csv.DictReader(f)
            for line in csv_reader:
                results.append(line)
        return results

    def get_rest_task(self):
        results = self.load_csv(self.result_path)
        index = 0
        for result in results:
            if result['is_crawled'] == '0':
                return index, results
            self.logger.debug('爬取公开号{}'.format(result['公开号']))
            index += 1
        return None

    def crawl_patents(self):
        session = webdriver.Chrome()
        while(True):
            index, results = self.get_rest_task()
            result = results[index]
            app_num = result['申请号']
            result['is_crawled'] = '1'
            if not app_num:
                break
            try:
                # 遍历专利搜索结果
                session.get(self.search_url)
                inp = session.find_element_by_id('search_input')
                inp.clear()
                inp.send_keys(app_num)
                sleep(2)
                inp.send_keys(Keys.ENTER)
                sleep(5)
                page_source = session.page_source
                sleep(5)
                select = Selector(text=page_source)
                tables = select.xpath("//div[@class='list-container']/ul/li")
                for table in tables:
                    invert_name = table.xpath(".//h1[@class='left']/div[2]/a/b/text()").extract_first()
                    table = table.xpath(".//div[@class='item-content-body left']")
                    app_date = table.xpath('p[2]/a/text()').extract_first()
                    pub_num = table.xpath('p[3]/text()').extract_first()
                    ipcs = table.xpath('p[5]/span/a/text()').extract()
                    ipc = self.merget_list(ipcs)
                    app_persons = table.xpath('p[6]/span/a/text()').extract()
                    app_persons = self.merget_list(app_persons)
                    inventors = table.xpath('p[7]/span/a/text()').extract()
                    inventors = self.merget_list(inventors)
                    is_exist = False
                    for item in results:
                        if item['申请号'] == result['申请号']:
                            if item['申请日'] == app_date:
                                if item['公开号'] == pub_num:
                                    is_exist = True
                    if is_exist:
                            continue
                    result['发明名称'] = invert_name
                    result['申请日'] = app_date
                    result['公开号'] = pub_num
                    result['IPC分类号'] = ipc
                    result['发明人'] = inventors
                    result['申请人'] = app_persons
                    self.logger.debug(u'发明名称 {0}, 申请日{1}, 公开号{2}, IPC分类号{3}, 发明人{4}, 申请人{5}'.format(result['发明名称'], result['申请日'], result['公开号'], result['IPC分类号'], result['发明人'], result['申请人']))
                    break
            except Exception as e:
                self.logger.exception(e)
            finally:
                self.store_to_file(results, self.result_path)
        session.quit()
        self.logger.info('crawl all task.')

    def store_to_file(self, results, path):
        with open(path, 'w') as f:
            fieldnames = [u'发明名称', u'申请号', u'申请日', u'公开号', u'IPC分类号', u'申请人', u'发明人', u'摘要', u'法律状态', u'is_crawled']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in results:
                writer.writerow({
                    u'发明名称': item['发明名称'],
                    u'申请号': item['申请号'],
                    u'申请日': item['申请日'],
                    u'公开号': item['公开号'],
                    u'IPC分类号': item['IPC分类号'],
                    u'申请人': item['申请人'],
                    u'发明人': item['发明人'],
                    u'摘要': '',
                    u'法律状态': '',
                    u'is_crawled': item['is_crawled']
                })
            writer.writerows(results)

    def merget_list(self, list):
        stream = ''
        for item in list:
            item = item.replace('\n', '').replace('\t', '')
            if len(item) != 0:
                stream += '{},'.format(item)
        return stream







