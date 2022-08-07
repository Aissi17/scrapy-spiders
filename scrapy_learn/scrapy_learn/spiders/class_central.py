import scrapy


class ClassCentralSpider(scrapy.Spider):
    name = 'class-central'
    allowed_domains = ['classcentral.com']
    start_urls = ['http://classcentral.com/']

    def parse(self, response):
        pass
