from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
import os

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class BooksSpider(Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]

    def start_requests(self):
        self.driver = webdriver.Chrome(
            f"{os.getcwd()}/scrapy_learn/assets/chromedriver"
        )
        self.driver.get("https://books.toscrape.com/")
        selector = Selector(text=self.driver.page_source)
        books = selector.xpath("//h3/a/@href").extract()
        for book in books:
            url = "https://books.toscrape.com/" + book
            yield Request(url, callback=self.parse_book)

        while True:
            try:
                next_page = self.driver.find_element(By.XPATH, '//a[text()="next"]')
                sleep(3)
                self.logger.info("Getting the next page ...")
                next_page.click()

                selector = Selector(text=self.driver.page_source)
                books = selector.xpath("//h3/a/@href").extract()
                for book in books:
                    url = "https://books.toscrape.com/catalogue/" + book
                    yield Request(url, callback=self.parse_book)
            except NoSuchElementException:
                self.logger.info("All pages were succefully scraped.")
                self.driver.quit()
                break

    def parse_book(self, reponse):
        pass
