import scrapy


class AtlassianSpider(scrapy.Spider):
    name = "atlassian"
    allowed_domains = ["atlassian.com"]
    start_urls = ["https://atlassian.com/agile"]
    max_depth = 2

    def parse(self, response):
        # Capture the current page
        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "body": response.text,
        }

        if response.meta.get("depth", 0) < self.max_depth:
            for href in response.css("a::attr(href)").getall():
                yield response.follow(href, callback=self.parse)
