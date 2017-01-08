# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from patents.settings import USER_AGENTS, PROXIES


class UserAgentMiddleware(object):
    """ update user agent for every request """
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENTS)
        request.headers['User-Agent'] = user_agent


# Start your middleware class
class ProxyMiddleware(object):
    def __init__(self):
        self.proxies = PROXIES

    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = 'http://{}'.format(random.choice(self.proxies))

