# -*- coding: utf-8 -*-
import scrapy
from pic.proxyPool.proxy import get_proxy


class TestproxySpider(scrapy.Spider):
    name = 'testProxy'
    allowed_domains = ['httpbin.org/get']
    start_urls = ['http://httpbin.org/get/']

    # def parse(self, response):
    #     print(response.text)
    #     pass

    def start_requests(self):
        url = 'http://httpbin.org/get'
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        # for i in range(4):
            # proxy = get_proxy()
            # print(proxy)
            # meta={'proxy': 'http://124.193.37.5:8888'}
            # yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={'proxy': 'http://124.193.37.5:8888'})

    def parse(self, response):
        print(response.text)
