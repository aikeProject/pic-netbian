#### `scrapy`爬取`http://pic.netbian.com/`的图片

#### 实现图片爬去分类
```python
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
```

#### 爬去每一个分页后面的所有分页数据图片
```python
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
            yield pic_item
```
#### 定义`items`,编写`items.py`
```python
from scrapy import Item, Field

class PicItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    href = Field()
    title = Field()
    downUrl = Field()
    sifyHref = Field()
    # 分类
    sifyName = Field()
```

#### 实现图片下载，保存到不同`分类`目录下面
- 编辑`pipelines.py`
```python
#  重写ImagesPipeline，实现下载图片

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
```

#### `settings`配置
```python
# 图片存储位置
IMAGES_STORE = 'D:\pic-netbian'
ITEM_PIPELINES = {
    # 图片下载的中间件
    'pic.pipelines.PicPipeline': 300,
}
```