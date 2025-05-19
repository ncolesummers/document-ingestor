import scrapy


class ScaledagileframeworkSpider(scrapy.Spider):
    name = "scaledagileframework"
    allowed_domains = ["scaledagileframework.com"]
    start_urls = ["https://scaledagileframework.com"]

    def parse(self, response):
        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "body": response.text,
        }

        if response.meta.get("depth", 0) < 2:
            for href in response.css("a::attr(href)").getall():
                url = response.urljoin(href)
                if url.startswith("https://") and "scaledagileframework.com" in url:
                    yield response.follow(url, callback=self.parse)
