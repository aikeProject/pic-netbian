# -*- coding: utf-8 -*-
import scrapy
import re
from pic.items import PicItem


class PicNetbianSpider(scrapy.Spider):
    name = 'netbian'
    allowed_domains = ['pic.netbian.com']
    start_urls = ['http://pic.netbian.com/']

    domain = 'http://pic.netbian.com'
    download = 'http://pic.netbian.com/e/extend/downpic.php?id={id}'
    downloadUrl = 'http://pic.netbian.com/downpic.php?id={id}'

    # cookies = {
    #     '__cfduid': 'dfe4cad6e8cd802496e52ebce437628811552023045',
    #     'Hm_lvt_526caf4e20c21f06a4e9209712d6a20e': '1552023046',
    #     'yjs_id': 'c98f486fedc6a648e533fab476f2ea5d',
    #     'ctrl_time': 1,
    #     'PHPSESSID': '359d8773dff8f0a7b776c0053d82fda1',
    #     'zkhanmlusername': '%B3%C9%D3%EA',
    #     'zkhanmluserid': '479261',
    #     'zkhanmlgroupid': '3',
    #     'zkhanmlrnd': '9tbNtbC95r5we6lojpTV',
    #     'zkhanmlauth': '5654075243395d2dc6040c1acec8f976',
    #     'security_session_verify': '04dfe61423a2c545878c072346c670e5',
    #     'Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e': '1552023054'
    # }

    def start_requests(self):
        yield scrapy.Request(
            url=self.domain,
            # cookies=self.cookies,
            callback=self.parse_sify
        )

    def parse_sify(self, response):
        # 获取分类
        classify = response.css('#main > div.classify a')
        for sify in classify:
            # 分类页对应的url
            sify_href = self.domain + sify.attrib['href']
            # 分类名
            sify_name = sify.css('::text').get()
            yield scrapy.Request(
                url=sify_href,
                cookies=self.cookies,
                callback=self.parse_item_sum,
                meta={
                    'sify_name': sify_name,
                    'sify_href': sify_href,
                }
            )

    # 爬取每一个分来下面的内容
    def parse_item_sum(self, response):
        # 分页总数
        sum = response.css('#main > div.page > span.slh + a::text').get()
        sum_int = int(sum)
        sify_href = response.meta['sify_href']
        sify_name = response.meta['sify_name']
        for i in range(1, sum_int + 1):
            if i == 1:
                url = sify_href
            else:
                url = sify_href + 'index_{i}.html'.format(i=i)
            yield scrapy.Request(
                url=url,
                callback=self.parse_item,
                meta={
                    'sify_name': sify_name,
                    'sify_href': sify_href,
                }
            )
    # 解析每一页数据
    def parse_item(self, response):
        result = response.css('.slist ul li')
        sify_href = response.meta['sify_href']
        sify_name = response.meta['sify_name']
        pic_item = PicItem()
        for item in result:
            href = item.css('a').attrib['href']
            id = re.compile('.*?(\d+).*?').match(href).group(1)
            pic_item['href'] = self.domain + item.css('a').attrib['href']
            pic_item['title'] = item.css('a b::text').get()
            pic_item['downUrl'] = self.downloadUrl.format(id=id)
            pic_item['sifyHref'] = sify_href
            pic_item['sifyName'] = sify_name
            pic_item['id'] = id
            yield pic_item
