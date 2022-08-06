from scrapy import Spider
from scrapy.http import Request


class BooksSpider(Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.xpath("//h3/a/@href").extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)
        # ? go to the next page
        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)

    def parse_book(self, response):
        title = response.xpath("//h1/text()").extract_first()
        price = response.xpath('//p[@class="price_color"]/text()').extract_first()
        image_url = response.xpath("//img/@src").extract_first()
        image_url = image_url.replace("../..", "https://books.toscrape.com/")
        rating = (
            response.xpath('//p[contains(@class,"star-rating")]/@class')
            .extract_first()
            .split(" ")[1]
        )
        description = response.xpath(
            '//*[@id="product_description"]/following-sibling::p/text()'
        ).extract_first()

        # product information

        yield {
            "title": title,
            "price": price,
            "image_url": image_url,
            "rating": rating,
            "description": description,
        }
