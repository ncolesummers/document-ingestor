from __future__ import annotations

from scrapy.cmdline import execute


def run_spider(name: str) -> None:
    """Execute a Scrapy spider by name."""
    execute(["scrapy", "crawl", name])


def crawl_atlassian() -> None:
    run_spider("atlassian")


def crawl_martinfowler() -> None:
    run_spider("martinfowler")


def crawl_mountaingoatsoftware() -> None:
    run_spider("mountaingoatsoftware")


def crawl_scaledagileframework() -> None:
    run_spider("scaledagileframework")


def crawl_scrumguides() -> None:
    run_spider("scrumguides")


def crawl_scrumalliance() -> None:
    run_spider("scrumalliance")
