import scrapy


class AtlassianSpider(scrapy.Spider):
    name = "atlassian"
    allowed_domains = ["atlassian.com"]
    start_urls = ["https://atlassian.com/agile"]

    def parse(self, response):
        # Capture the current page
        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "body": response.text,
        }

        # Follow in-site links up to depth 2
        if response.meta.get("depth", 0) < 2:
            for href in response.css("a::attr(href)").getall():
                url = response.urljoin(href)
                if url.startswith("https://") and "atlassian.com" in url:
                    yield response.follow(url, callback=self.parse)
