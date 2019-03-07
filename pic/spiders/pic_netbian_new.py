# -*- coding: utf-8 -*-
import json
import requests
import scrapy
import re
import os
from hashlib import md5
from pic.items import PicItem


class PicNetbianSpider(scrapy.Spider):
    name = 'pic_netbian'
    allowed_domains = ['pic.netbian.com']
    start_urls = ['http://pic.netbian.com/']

    domain = 'http://pic.netbian.com'
    download = 'http://pic.netbian.com/e/extend/downpic.php?id={id}'
    downloadUrl = 'http://pic.netbian.com/downpic.php?id={id}'

    headers = {
        'Cookie': '__cfduid=db1d046d01386264a48a1f8871276deb71551795808; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1551795811; yjs_id=74b8ba017da09aeddd8b20ed18021308; ctrl_time=1; PHPSESSID=cdb42cc013d05a0701334818bdc73ff8; zkhanmlusername=%B3%C9%D3%EA; zkhanmluserid=479261; zkhanmlgroupid=1; zkhanmlrnd=tgCOOvuHDUhiEbFEAm1X; zkhanmlauth=6f9d209428366009cfb399f561ee5774; zkhanpayphome=BuyGroupPay; zkhanpaymoneybgid=1; security_session_verify=ffb36d8046e9e7f96b024492dd50ad55; Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1551802772'
    }

    cookies = {
        '__cfduid': 'db1d046d01386264a48a1f8871276deb71551795808',
        'Hm_lvt_526caf4e20c21f06a4e9209712d6a20e': '1551795811',
        'yjs_id': '74b8ba017da09aeddd8b20ed18021308',
        'ctrl_time': 1,
        'PHPSESSID': 'cdb42cc013d05a0701334818bdc73ff8',
        'zkhanmlusername': '%B3%C9%D3%EA',
        'zkhanmluserid': '479261',
        'zkhanmlgroupid': '1',
        'zkhanmlrnd': 'tgCOOvuHDUhiEbFEAm1X',
        'zkhanmlauth': '6f9d209428366009cfb399f561ee5774',
        'security_session_verify': 'ffd2fd3a71cb24f6d9bcc6394b36b4b6',
        'Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e': '1551801638'
    }

    # pool = Pool()

    # 默认爬取跳转url
    def parse(self, response):
        result = response.css('.slist ul li')
        pic_item = PicItem()
        for item in result:
            href = item.css('a').attrib['href']
            id = re.compile('.*?(\d+).*?').match(href).group(1)
            pic_item['href'] = item.css('a').attrib['href']
            pic_item['title'] = item.css('a b::text').get()
            pic_item['downUrl'] = self.downloadUrl.format(id=id)
            yield pic_item

        next = response.css('#main > div.page > a:nth-child(13)').attrib['href']
        if next is not None:
            yield scrapy.Request(
                url=self.domain + next,
                callback=self.parse
            )
