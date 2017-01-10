# -*- coding: utf-8 -*-
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
            path = '{}.csv'.format(company)
            #self.crawl_app_nums(company, path)
            self.crawl_patents(path)

    def crawl_app_nums(self, company, path):
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
        self.logger.info(u'[{0}]: max page: {1}, total: {2}'.format(company, max_page, total))

        # 遍历多页得到专利申请号
        app_nums = []
        for page in xrange(1, max_page + 1):
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
                items = select.xpath("//div[@class='item-content-body left']/p[1]/text()").extract()
                app_nums.extend(items)
                self.logger.info('crawl page: {} success.'.format(page))
            except Exception as e:
                self.logger.error(e)
                self.logger.info('crawl page: {} failed.'.format(page))
                continue
        results = []
        # 申请号，去重。并根据申请号生成爬取清单。
        app_nums = list(set(app_nums))
        for app_num in app_nums:
            result = {
                '发明名称': '',
                '申请号': app_num,
                '申请日': '',
                '公开号': '',
                'IPC分类号': '',
                '申请人': '',
                '发明人': '',
                '摘要': '',
                '法律状态': '',
                'is_crawled': '0'
            }
            results.append(result)
        self.store_to_file(results, path)
        self.logger.info('crawl all task.')
        session.quit()

    def load_csv(self, path):
        results = []
        with open(path, 'r') as f:
            csv_reader = csv.DictReader(f)
            for line in csv_reader:
                results.append(line)
        return results

    def get_rest_task(self, path):
        results = self.load_csv(path)
        index = 0
        for result in results:
            if result['is_crawled'] == '0':
                return index, results
            self.logger.debug('爬取申请号{}'.format(result['申请号']))
            index += 1
        return None

    def crawl_patents(self, path):
        session = webdriver.Chrome()
        session.implicitly_wait(10)
        now_handle = session.current_window_handle
        while(True):
            # 关闭全部子窗口
            all_handles = session.window_handles
            for handle in all_handles:
                if handle != now_handle:
                    session.switch_to_window(handle)
                    sleep(2)
                    session.close()
            # 切换到主窗口
            session.switch_to_window(now_handle)
            index, results = self.get_rest_task(path)
            result = results[index]
            app_num = result['申请号']
            result['is_crawled'] = '1'
            if not app_num:
                break
            try:
                # 进入搜索页面
                session.get(self.search_url)
                inp = session.find_element_by_id('search_input')
                inp.clear()
                inp.send_keys(app_num)
                sleep(1)
                inp.send_keys(Keys.ENTER)
                sleep(20)
                # 进入搜索结果页面
                session.find_element_by_xpath("//a[@role='detail']").click()
                # 进入单个专利页面
                sleep(5)
                session.switch_to_window(session.window_handles[1])
                sleep(1)
                # 解析单个专利
                pagesource = session.page_source
                select = Selector(text=pagesource)
                result['发明名称'] = select.xpath("//*[@id='tabContent_1_id']/div[1]/text()").extract_first()
                trs = select.xpath("//div[@class='table-container']/table/tbody/tr")
                for tr in trs:
                    key = tr.xpath("td[@class='first-td']/div/text()").extract_first()
                    value = tr.xpath("td[@class='second-td']/div/text()").extract_first()
                    if key == u'申请日':
                        result['申请日'] = value
                    elif key == u'公开（公告）号':
                        result['公开号'] = value
                    elif key == u'IPC分类号':
                        result['IPC分类号'] = value
                    elif key == u'申请（专利权）人':
                        result['申请人'] = value
                    elif key == u'发明人':
                        result['发明人'] = value
                result['摘要'] = select.xpath("//*[@id='cpp_content_i0j0']/p/text()").extract_first()
                self.logger.debug(u'申请号 {}, 申请日 {}, 公开号 {}, IPC分类号 {}, 申请人 {}, 发明人 {}, 摘要 {}'.format(
                    result['申请号'], result['申请日'], result['公开号'], result['IPC分类号'], result['申请人'], result['发明人'], result['摘要']
                ))
            except Exception as e:
                self.logger.exception(e)
            finally:
                self.store_to_file(results, path)
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
                    u'摘要': item['摘要'],
                    u'法律状态': '',
                    u'is_crawled': item['is_crawled']
                })
