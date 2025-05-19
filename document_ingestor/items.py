# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DocumentIngestorItem(scrapy.Item):
    """Common structure for pages collected by all spiders."""

    title = scrapy.Field()
    url = scrapy.Field()
    body_text = scrapy.Field()
    source = scrapy.Field()
    retrieved_at = scrapy.Field()
