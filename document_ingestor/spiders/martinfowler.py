import scrapy


class MartinfowlerSpider(scrapy.Spider):
    name = "martinfowler"
    allowed_domains = ["martinfowler.com"]
    start_urls = ["https://martinfowler.com"]
    max_depth = 2

    def parse(self, response):
        if response.url.rstrip("/").endswith("agile.html"):
            for href in response.css("a::attr(href)").getall():
                yield response.follow(href, callback=self.parse_article)
        else:
            yield {
                "url": response.url,
                "title": response.css("title::text").get(),
                "body": response.text,
            }

            if response.meta.get("depth", 0) < self.max_depth:
                for href in response.css("a::attr(href)").getall():
                    yield response.follow(href, callback=self.parse)

            if response.url.rstrip("/") == "https://martinfowler.com":
                yield response.follow("/agile.html", callback=self.parse)

    def parse_article(self, response):
        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "body": response.text,
        }
