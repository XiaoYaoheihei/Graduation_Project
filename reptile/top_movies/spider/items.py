# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    title = scrapy.Field()    # 电影标题
    rating = scrapy.Field()   # 评分
    votes = scrapy.Field()    # 评价人数
    quote = scrapy.Field()    # 经典台词
    link = scrapy.Field()     # 详情链接
