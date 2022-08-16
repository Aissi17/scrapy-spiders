import scrapy
from scrapy.http import Request


class ClassCentralSpider(scrapy.Spider):
    name = "class-central"
    allowed_domains = ["classcentral.com"]
    start_urls = ["http://classcentral.com/subjects"]

    def __init__(
        self,
        subject=None,
    ):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            subject_url = response.xpath(
                f"//span[contains(text(),'{self.subject}')]/../@href"
            ).extract_first()

            yield Request(response.urljoin(subject_url), callback=self.parse_subject)
        else:
            subjects = response.xpath(
                '//*[@id="page-subjects"]/div[1]/section[2]/ul/li/h3/a/@href'
            ).extract()

            for subject in subjects:
                yield Request(response.urljoin(subject), callback=self.parse_subject)

    def parse_subject(self, response):
        subject_name = (
            response.xpath("//title/text()").extract_first().strip().split("|")[0]
        )

        # title = response.xpath(
        #     '//a[contains(@class,"course-name")]/h2/text()'
        #     #'//h2[@itemprop="name"]/text()'
        # ).extract()

        courses = response.xpath('//a[contains(@class,"course-name")]')
        for cours in courses:
            course_name = cours.xpath(".//h2/text()").extract_first()
            course_url = cours.xpath(".//@href").extract_first()
            absolute_course_url = response.urljoin(course_url)

            yield {
                "subject_name": subject_name,
                "course_name": course_name,
                "absolute_course_url": absolute_course_url,
            }
        next_page = response.xpath("//*[@rel='next']/@href").extract_first()
        yield Request(response.urljoin(next_page), callback=self.parse_subject)
