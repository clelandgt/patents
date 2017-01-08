# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import logging
from patents.settings import USER_AGENTS, PROXIES


class UserAgentMiddleware(object):
    """ update user agent for every request """
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENTS)
        request.headers['User-Agent'] = user_agent


# Start your middleware class
class ProxyMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.proxies = PROXIES

    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        proxy = 'http://{}'.format(random.choice(self.proxies))
        request.meta['proxy'] = proxy
        company_name = request.meta.get('company', '')
        self.logger.debug(u'crawl {0} with proxy {1}'.format(company_name, proxy))

