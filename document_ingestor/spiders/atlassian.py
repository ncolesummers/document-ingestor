import scrapy


class AtlassianSpider(scrapy.Spider):
    name = "atlassian"
    allowed_domains = ["atlassian.com"]
    start_urls = ["https://atlassian.com"]

    def parse(self, response):
        pass
