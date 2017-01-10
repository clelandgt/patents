# 抓取公司专利信息

##待抓取的公司
- 卡斯柯信号有限公司
- 北京全路通信信号研究设计院\ 北京全路通信信号研究设计院集团有限公司\北京全路通信信号研究设计院有限公司
- 上海富欣智能交通控制有限公司
- 北京交控科技股份有限公司
- 北京和利时系统工程有限公司
- 中国铁道科学研究院通信信号研究所
- 南京恩瑞特实业有限公司
- 北京交大微联科技有限公司
- 浙江众合科技股份有限公司\浙江众合机电股份有限公司
- 上海亨钧科技股份有限公司\上海亨钧科技股份有限公司

##输出
文件格式：csv
内容格式:
| 序号 | 发明名称 | 申请号 | 申请日 | 公开号 | IPC分类号 | 申请人 | 发明人 | 摘要 | 法律状态 |
| --  |

##项目结构
patents/
├── README.md
├── doc
│   ├── 专利.xlsx
│   └── 公司名称.txt
├── patents
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── items.py
│   ├── items.pyc
│   ├── middlewares.py
│   ├── middlewares.pyc
│   ├── pipelines.py
│   ├── settings.py
│   ├── settings.pyc
│   └── spiders
│       ├── __init__.py
│       ├── __init__.pyc
│       ├── patents_spider.py
│       └── patents_spider.pyc
├── patents.log
└── scrapy.cfg

##安装使用说明
###配置环境和运行
首先确认已经安装python和pip安装包管理工具
1.安装scrapy
    $ pip install scrapy
2.安装selenium
    $ pip install selenium
3.安装chromedriver
    $ pip install chromedriver
4.进入主目录，运行爬虫：
    $ scrapy crawl patents_spider

###使用说明
前期以为反爬虫不厉害，计划使用scrapy框架，模拟request请求，做爬虫。后面碰到遇到一些问题:
1.频繁出现302，网站响应速度慢；
2.专利详览按钮中使用动态加载js获取页面，不能直接获取url地址。
基于以上原因，采用selenium模拟浏览器，基本没有使用scrapy框架，只是套用一个空壳子，所以核心代码只有：patents/patents/spiders/patents_spider.py。
####设计思路
先爬取一个公司所有的专利申请号，然后再根据专利申请号去爬取该专利的详细信息。
爬取结果表中有一个is_crawled列，初始状态值是0，爬取后会变为1. 如果需要重新爬取某个专利的结果，只需要把该列状态值变为0. 重新启动项目时，会自动该列爬取状态值为0的行。

####核心代码
1. company_list 配置需要爬取的公司
    company_list = [
        u'卡斯柯信号有限公司',
        # u'北京全路通信信号研究设计院',
        ...
    ]
2.爬取的入口函数：
    start_requests， 其中有详细注释。
3.爬取一个公司所有专利的申请号
    crawl_app_nums
4.爬取专利的详细信息
    crawl_patents


