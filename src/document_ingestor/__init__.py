"""document-ingestor package."""

from .main import main
from .crawler import Crawler, crawl_from_config

__all__ = ["main", "Crawler", "crawl_from_config"]
