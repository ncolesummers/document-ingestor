import scrapy


class ScaledagileframeworkSpider(scrapy.Spider):
    name = "scaledagileframework"
    allowed_domains = ["scaledagileframework.com"]
    start_urls = ["https://scaledagileframework.com"]
    max_depth = 2

    def parse(self, response):
        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "body": response.text,
        }

        if response.meta.get("depth", 0) < self.max_depth:
            for href in response.css("a::attr(href)").getall():
                yield response.follow(href, callback=self.parse)
