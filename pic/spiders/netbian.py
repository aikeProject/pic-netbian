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

    def start_requests(self):
        yield scrapy.Request(
            url=self.domain,
            cookies=self.cookies,
            callback=self.parse_sify
        )

    def parse_sify(self, response):
        # 获取分类
        classify = response.css('#main > div.classify a')
        for sify in classify:
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
            yield pic_item
