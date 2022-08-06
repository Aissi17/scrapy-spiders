import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        h1_text = response.xpath("//h1/a/text()").extract_first()
        all_tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()
        yield {"H1 text": h1_text, "Tags": all_tags}
