import scrapy
from spider.items import SpiderItem

class DoubanTopMoviesSpider(scrapy.Spider):
    name = 'douban_top_movies'
    allowed_domains = ['movie.douban.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # 请求间隔
        'CONCURRENT_REQUESTS': 1,  # 并发请求数
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://movie.douban.com/',
        }
    }

    def start_requests(self):
        # for page in range(0, 4):  # 爬取4页获取100条数据
        url = f'https://movie.douban.com/top250?start=25'
        yield scrapy.Request(
            url=url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            callback=self.parse
        )

    def parse(self, response):
        for item in response.css('.item'):
            movie = SpiderItem()
            
            movie['title'] = item.css('.title::text').get()
            movie['rating'] = item.css('.rating_num::text').get()
            movie['votes'] = item.css('.star>span:last-child::text').re_first(r'\d+')
            movie['quote'] = item.css('.inq::text').get()
            movie['link'] = item.css('a::attr(href)').get()
            
            yield movie
