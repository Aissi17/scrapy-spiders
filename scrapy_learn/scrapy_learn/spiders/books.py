from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BooksSpider(CrawlSpider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]
    rules = [
        Rule(LinkExtractor(), callback="parse", follow=False),
    ]

    def parse(self, response):
        pass
