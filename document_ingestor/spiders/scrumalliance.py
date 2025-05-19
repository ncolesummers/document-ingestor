import scrapy


class ScrumallianceSpider(scrapy.Spider):
    name = "scrumalliance"
    allowed_domains = ["resources.scrumalliance.org"]
    start_urls = ["https://resources.scrumalliance.org"]

    def parse(self, response):
        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "body": response.text,
        }

        if response.meta.get("depth", 0) < 1:
            for href in response.css("a::attr(href)").getall():
                url = response.urljoin(href)
                if url.startswith("https://") and "resources.scrumalliance.org" in url:
                    yield response.follow(url, callback=self.parse)
