# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from patents.settings import USER_AGENTS


class UserAgentMiddleware(object):
    """ update user agent for every request """
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENTS)
        request['User-Agent'] = user_agent
