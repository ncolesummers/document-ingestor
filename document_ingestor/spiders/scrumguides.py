import scrapy


class ScrumguidesSpider(scrapy.Spider):
    name = "scrumguides"
    allowed_domains = ["scrumguides.org"]
    start_urls = ["https://scrumguides.org/docs/scrumguide"]

    def parse(self, response):
        pass
