import scrapy


class ScrumguidesSpider(scrapy.Spider):
    name = "scrumguides"
    allowed_domains = ["scrumguides.org"]
    start_urls = ["https://scrumguides.org/docs/scrumguide"]
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
