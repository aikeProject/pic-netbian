# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import re

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
# from

class PicPipeline(ImagesPipeline):
    cookies = {
        '__cfduid': 'dfe4cad6e8cd802496e52ebce437628811552023045',
        'Hm_lvt_526caf4e20c21f06a4e9209712d6a20e': '1552023046',
        'yjs_id': 'c98f486fedc6a648e533fab476f2ea5d',
        'ctrl_time': 1,
        'PHPSESSID': '359d8773dff8f0a7b776c0053d82fda1',
        'zkhanmlusername': '%B3%C9%D3%EA',
        'zkhanmluserid': '479261',
        'zkhanmlgroupid': '3',
        'zkhanmlrnd': '9tbNtbC95r5we6lojpTV',
        'zkhanmlauth': '5654075243395d2dc6040c1acec8f976',
        'security_session_verify': '04dfe61423a2c545878c072346c670e5',
        'Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e': '1552023054'
    }

    def get_media_requests(self, item, info):
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        try:
            yield Request(item['downUrl'], cookies=self.cookies, meta={'name': item['sifyName']})
        except:
            print('又被封了...')

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

    def get_images(self, response, request, info):
        print('images---')
        pass

# mongodb
class MongoPipeline(object):
    collection_name = 'users'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].update({'id': item['id']}, dict(item), True)
        return item
