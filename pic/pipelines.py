# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class PicPipeline(ImagesPipeline):
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

    def get_media_requests(self, item, info):
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        yield Request(item['downUrl'], cookies=self.cookies, meta={'name': item['sifyName']})

    # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    def file_path(self, request, response=None, info=None):
        # 提取url前面名称作为图片名。
        image_guid = request.url.split('?id=')[-1]
        # print(image_guid)
        # 接收上面meta传递过来的图片名称
        name = request.meta['name']
        # 过滤windows字符串，不经过这么一个步骤，你会发现有乱码或无法下载
        name = re.sub(r'[？\\*|“<>:/]', '', name)
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        filename = '{0}/{1}.jpg'.format(name, image_guid)
        return filename
