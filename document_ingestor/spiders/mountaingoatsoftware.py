import scrapy


class MountaingoatsoftwareSpider(scrapy.Spider):
    name = "mountaingoatsoftware"
    allowed_domains = ["mountaingoatsoftware.com"]
    start_urls = ["https://mountaingoatsoftware.com"]

    def parse(self, response):
        pass
