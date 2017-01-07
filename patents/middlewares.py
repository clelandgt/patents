# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import ast
import random
import requests
from patents.settings import USER_AGENTS, PROXY_API


class UserAgentMiddleware(object):
    """ update user agent for every request """
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENTS)
        request.headers['HOST'] = 'www.pss-system.gov.cn'
        request.headers['User-Agent'] = user_agent


class UserAgentMiddleware(object):
    proxies = []

    def process_request(self, request, spider):
        proxy = self.get_proxies()
        request.meta['proxy'] = 'http://{}'.format(proxy)
        print request.meta['proxy']

    def get_proxies(self):
        if len(self.proxies) != 0:
            return self.pop_proxy(self.proxies)
        response = requests.get(PROXY_API)
        proxies = ast.literal_eval(response.text)[:50]
        proxies = set(proxies)
        self.proxies.extend(proxies)
        return self.pop_proxy(self.proxies)

    def pop_proxy(self, proxies):
        proxy = random.choice(proxies)
        self.proxies.remove(proxy)
        return proxy


