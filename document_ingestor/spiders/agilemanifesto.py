import scrapy


class AgilemanifestoSpider(scrapy.Spider):
    name = "agilemanifesto"
    allowed_domains = ["agilemanifesto.org"]
    start_urls = ["https://agilemanifesto.org"]

    def parse(self, response):
        pass
