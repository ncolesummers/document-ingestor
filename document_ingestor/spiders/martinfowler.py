import scrapy


class MartinfowlerSpider(scrapy.Spider):
    name = "martinfowler"
    allowed_domains = ["martinfowler.com"]
    start_urls = ["https://martinfowler.com"]

    def parse(self, response):
        pass
