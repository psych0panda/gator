# -*- coding: utf-8 -*-
import scrapy
import time
import json

from ..items import BaseItem


class NineGagSpider(scrapy.Spider):
    name = 'nine_gag'
    allowed_domains = ['9gag.com']
    start_urls = ['https://9gag.com/v1/group-posts/group/default/type/hot?']

    def parse(self, response):
        item = BaseItem()
        json_response = json.loads(response.body_as_unicode())
        posts = json_response['data']['posts']
        for post in posts:
            item['data'] = post
            yield item
        try:
            next_cursor = json_response['data']['nextCursor']
        except KeyError:
            print("\n\tno_more_results\n")
        next_page = self.start_urls[0] + next_cursor
        yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def get_posts_by_date(from_date: int = time.time() - 86400,
                          to_date: int = time.time(),
                          post_date: int = None) -> bool:
        if int(from_date) <= int(post_date) <= int(to_date):
            return True
        else:
            return False
