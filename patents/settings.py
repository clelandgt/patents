# -*- coding: utf-8 -*-

# Scrapy settings for patents project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os


BOT_NAME = 'patents'

SPIDER_MODULES = ['patents.spiders']
NEWSPIDER_MODULE = 'patents.spiders'


# Configure logging
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'patents.log'

# Set delay time for request
DOWNLOAD_DELAY = 10
DOWNLOAD_TIMEOUT = 20

# Retry if download failed
RETRY_TIMES = 100
RETRY_HTTP_CODES = [500, 503, 502, 504, 403, 400, 302, 303]

# Turn off redirect
REDIRECT_ENABLED = False
COOKIES_ENABLED = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'patents (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'patents.middlewares.PatentsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
   'patents.middlewares.ProxyMiddleware': 100,
   'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
   'patents.middlewares.UserAgentMiddleware': 120,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'patents.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Configure request headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Host': 'www.pss-system.gov.cn',
    'Origin': 'http://www.pss-system.gov.cn',
    'Referer': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/searchHomeIndex-searchHomeIndex.shtml',
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
}

# Configure ip proxy
PROXIES = [
    "94.177.175.105:1453",
    "89.40.113.128:2016",
    "168.9.128.3:65000",
    "106.2.187.202:8080",
    "1.82.216.134:80",
    "58.217.195.141:80",
    "218.106.205.145:8080",
    "1.82.216.135:80",
    "116.240.96.84:3128",
    "165.138.65.233:3128",
    "168.9.128.4:65000",
    "61.191.41.130:80",
    "223.68.1.38:8000",
    "217.33.216.114:8080",
    "59.46.2.207:8888",
    "111.13.109.27:80",
    "204.29.115.149:8080",
    "222.201.132.32:3128",
    "190.121.228.83:3128",
    "168.9.128.144:65000",
    "61.161.140.171:8080",
    "192.34.58.204:3128",
    "123.5.57.136:9999",
    "218.103.60.205:8080",
    "61.129.129.72:8080",
    "182.48.114.49:8080",
    "167.114.167.221:3128",
    "123.234.219.133:8080",
    "200.29.191.149:3128",
    "120.132.71.212:80",
    "59.47.125.10:9797",
    "123.138.89.131:9999",
    "183.185.3.12:9797",
    "91.195.183.54:3128",
    "91.195.183.57:3128",
    "180.183.102.113:8080",
    "1.9.171.51:800",
    "218.56.132.156:8080",
    "125.31.19.26:80",
    "203.156.126.55:3129",
    "183.63.110.202:3128",
    "188.166.179.244:8080",
    "163.172.211.141:3128",
    "221.204.101.103:9797",
    "222.41.113.43:8080",
    "221.1.201.142:9797",
    "50.195.87.91:8080",
    "37.59.37.41:3128",
    "114.33.243.177:8080",
    "101.254.188.198:8080",
    "210.68.95.62:3128",
    "91.189.36.132:8080",
    "154.127.52.157:8080",
    "108.61.185.109:5555",
    "115.231.105.109:8081",
    "113.161.88.153:8080",
    "94.19.50.41:8080",
    "124.193.85.88:8080",
    "45.32.43.217:8081",
    "27.191.234.69:9999",
    "122.155.3.143:3128",
    "210.101.131.231:8080",
    "218.232.109.137:8090",
    "36.234.189.93:3128",
    "201.20.93.54:8080",
    "84.200.85.55:8888",
    "58.59.68.91:9797",
    "1.163.137.229:3128",
    "128.199.229.21:3128",
    "119.55.89.142:9999",
    "218.56.132.155:8080",
    "119.52.11.14:9999",
    "149.202.152.171:443",
    "50.93.202.32:1080",
    "120.76.203.31:80",
    "103.10.228.63:8080",
    "112.126.65.193:80",
    "149.154.137.205:8080",
    "1.163.154.77:3128",
    "37.205.63.19:8080",
    "185.28.193.95:8080",
    "128.199.158.131:80",
    "77.243.125.86:8080",
    "49.1.244.139:3128",
    "112.199.65.190:3128",
    "220.143.169.169:3128",
    "173.254.197.87:1080",
    "122.71.133.127:8080",
    "91.195.230.44:8080",
    "183.131.151.208:80",
    "94.177.251.159:2016",
    "138.201.63.123:31288",
    "61.223.116.80:3128",
    "195.246.57.154:8080",
    "121.15.254.149:808",
    "61.223.126.131:3128",
    "220.143.199.243:3128",
    "202.138.241.62:8080",
    "80.55.86.174:8080",
    "83.239.88.170:8080",
    "180.250.182.50:8080",
    "128.199.69.153:8080",
    "50.93.203.31:1080",
    "192.99.128.170:8080",
    "216.39.143.96:4440",
    "103.240.8.2:8080",
    "113.66.141.212:9797",
    "36.234.113.182:3128",
    "118.172.205.85:8080",
    "202.73.51.102:8128",
    "89.145.188.122:8080",
    "211.75.115.20:80",
    "190.104.245.39:8080",
    "118.171.10.219:3128",
    "27.131.47.132:9797",
    "177.87.10.166:8080",
    "211.152.62.226:80"
]


USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1"]
