import scrapy


class MountaingoatsoftwareSpider(scrapy.Spider):
    name = "mountaingoatsoftware"
    allowed_domains = ["mountaingoatsoftware.com"]
    start_urls = ["https://mountaingoatsoftware.com"]
    max_depth = 1

    def parse(self, response):
        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "body": response.text,
        }

        if response.meta.get("depth", 0) < self.max_depth:
            for href in response.css("a::attr(href)").getall():
                yield response.follow(href, callback=self.parse)
