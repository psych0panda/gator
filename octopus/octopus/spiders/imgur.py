# -*- coding: utf-8 -*-
import scrapy
import json

from ..items import BaseItem


class ImgurSpider(scrapy.Spider):
    name = 'imgur'
    allowed_domains = ['imgur.com']
    start_urls = [
        'https://api.imgur.com/3/gallery/hot/viral/0?IMGURPLATFORM=web&IMGURUIDJAFO'
        '=b25b186b7cbf8f4d0ef8d22e6cd27273507f61a98080fdc49a3f20ab8276e07b&SESSIONCOUNT=4&client_id=546c25a59c58ad7'
        '&realtime_results=false&showViral=true']

    def parse(self, response):
        item = BaseItem()
        json_response = json.loads(response.body_as_unicode())
        data = json_response['data']
        depth = 2
        num_page = 0
        for _ in range(depth):
            num_page += 1
            next_page = f'https://api.imgur.com/3/gallery/hot/viral/' \
                        f'{num_page}?IMGURPLATFORM=web&IMGURUIDJAFO' \
                        f'=b25b186b7cbf8f4d0ef8d22e6cd27273507f61a98080fdc49a3f20ab8276e07b&SESSIONCOUNT=4&client_id' \
                        f'=546c25a59c58ad7&realtime_results=false&showViral=true '
            for post in data:
                item['data'] = post
                yield item
            yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def json_writer(data=None, file='results/imgur.json') -> json:
        with open(file, mode='w+') as f:
            f.write(json.dumps(data, sort_keys=True,
                               indent=4, ensure_ascii=False))
