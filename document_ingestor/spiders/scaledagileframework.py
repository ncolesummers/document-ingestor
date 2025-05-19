import scrapy


class ScaledagileframeworkSpider(scrapy.Spider):
    name = "scaledagileframework"
    allowed_domains = ["scaledagileframework.com"]
    start_urls = ["https://scaledagileframework.com"]

    def parse(self, response):
        pass
