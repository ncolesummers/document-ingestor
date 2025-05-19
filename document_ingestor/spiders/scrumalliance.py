import scrapy


class ScrumallianceSpider(scrapy.Spider):
    name = "scrumalliance"
    allowed_domains = ["resources.scrumalliance.org"]
    start_urls = ["https://resources.scrumalliance.org"]

    def parse(self, response):
        pass
