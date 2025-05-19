import scrapy


class MartinfowlerSpider(scrapy.Spider):
    name = "martinfowler"
    allowed_domains = ["martinfowler.com"]
    start_urls = ["https://martinfowler.com"]

    def parse(self, response):
        if response.url.rstrip("/").endswith("agile.html"):
            for href in response.css("a::attr(href)").getall():
                url = response.urljoin(href)
                if url.startswith("https://") and "martinfowler.com" in url:
                    yield response.follow(url, callback=self.parse_article)
        else:
            yield {
                "url": response.url,
                "title": response.css("title::text").get(),
                "body": response.text,
            }

            # If this is the root page, jump to agile guide
            if response.url.rstrip("/") == "https://martinfowler.com":
                yield response.follow("/agile.html", callback=self.parse)

    def parse_article(self, response):
        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "body": response.text,
        }
