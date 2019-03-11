# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from pic.proxyPool.proxy import get_proxy


class PicSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


"""
添加随机ip代理并且设置cookie
"""


class PicDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):
        self.cookies = {
            '__cfduid': 'dfe4cad6e8cd802496e52ebce437628811552023045',
            'Hm_lvt_526caf4e20c21f06a4e9209712d6a20e': '1552023046,1552278580',
            'yjs_id': 'c98f486fedc6a648e533fab476f2ea5d',
            'ctrl_time': 1,
            'PHPSESSID': '359d8773dff8f0a7b776c0053d82fda1',
            'zkhanmlusername': '%B3%C9%D3%EA',
            'zkhanmluserid': '479261',
            'zkhanmlgroupid': '3',
            'zkhanmlrnd': 'Tu5P7keCmYDM2drWPqph',
            'zkhanmlauth': '5ed08d4b4e208c6de012dd282ca92594',
            'security_session_verify': 'f4e623de9fefb0013ca72e8161d5b364',
            'Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e': '1552280282'
        }

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 获取爬去下来的免费代理ip
        proxy = get_proxy()
        print('proxy--', proxy)
        # print('cookie--', self.cookies)
        if proxy:
            # request.meta['proxy'] = "http://{proxy}".format(proxy=proxy)
            request.meta['proxy'] = "http://{proxy}".format(proxy=proxy)

        # 设置cookie
        request.cookies = self.cookies

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 检测代理
class ProxyMiddleware(object):
    '''
    设置Proxy
    '''

    def process_request(self, request, spider):
        ip = get_proxy()
        print('ip--', ip)
        print('proxy--', "http://{proxy}".format(proxy=ip))
        request.meta['proxy'] = "http://{proxy}".format(proxy=ip)
