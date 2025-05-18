from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yaml = None


@dataclass
class DocumentRecord:
    url: str
    path: str
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    sha256: Optional[str] = None
    status: str = "fetched"


class Crawler:
    """Scrapy-based HTTP crawler that respects caching headers."""

    def __init__(self, config_path: Path) -> None:
        self.config_path = Path(config_path)
        with self.config_path.open("r", encoding="utf-8") as f:
            if self.config_path.suffix in {".yaml", ".yml"}:
                if yaml is None:
                    raise RuntimeError("PyYAML is required for YAML configs")
                config = yaml.safe_load(f)
            else:
                config = json.load(f)

        self.seed_urls: List[str] = config.get("seed_urls", [])
        output_dir = config.get("output_dir", "data/raw")
        self.output_dir = Path(output_dir)
        metadata_path = config.get("metadata_path", "crawl_metadata.json")
        self.metadata_path = Path(metadata_path)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata: Dict[str, Dict[str, str]] = {}
        if self.metadata_path.exists():
            with self.metadata_path.open("r", encoding="utf-8") as m:
                self.metadata = json.load(m)

    def _build_headers(self, url: str) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        entry = self.metadata.get(url)
        if not entry:
            return headers
        if etag := entry.get("etag"):
            headers["If-None-Match"] = etag
        if last := entry.get("last_modified"):
            headers["If-Modified-Since"] = last
        return headers

    def _filename_for_url(self, url: str) -> str:
        return hashlib.sha256(url.encode()).hexdigest()

    def crawl(self) -> List[DocumentRecord]:
        """Fetch all seed URLs using Scrapy."""

        self.records: List[DocumentRecord] = []

        crawler_self = self

        class FetchSpider(scrapy.Spider):
            name = "fetch_spider"

            def __init__(self, **kwargs: object) -> None:
                super().__init__(**kwargs)
                self.start_urls = crawler_self.seed_urls

            def start_requests(self):  # type: ignore[override]
                for url in self.start_urls:
                    headers = crawler_self._build_headers(url)
                    yield Request(url, headers=headers, meta={"original_url": url})

            def parse(self, response):  # type: ignore[override]
                url = response.meta["original_url"]
                if response.status == 304:
                    meta = crawler_self.metadata.get(url, {})
                    record = DocumentRecord(
                        url=url,
                        path=meta.get("path", ""),
                        etag=meta.get("etag"),
                        last_modified=meta.get("last_modified"),
                        sha256=meta.get("sha256"),
                        status="skipped",
                    )
                    crawler_self.records.append(record)
                    return

                content = response.body
                etag_bytes = response.headers.get("ETag")
                last_bytes = response.headers.get("Last-Modified")
                etag = etag_bytes.decode() if etag_bytes else None
                last_modified = last_bytes.decode() if last_bytes else None
                sha256 = hashlib.sha256(content).hexdigest()
                filename = crawler_self._filename_for_url(url)
                path = crawler_self.output_dir / filename
                path.write_bytes(content)
                record = DocumentRecord(
                    url=url,
                    path=str(path),
                    etag=etag,
                    last_modified=last_modified,
                    sha256=sha256,
                )
                crawler_self.records.append(record)
                crawler_self.metadata[url] = {
                    "path": str(path),
                    "etag": etag or "",
                    "last_modified": last_modified or "",
                    "sha256": sha256,
                }

        process = CrawlerProcess(settings={"LOG_ENABLED": False})
        process.crawl(FetchSpider)
        process.start()

        with self.metadata_path.open("w", encoding="utf-8") as m:
            json.dump(self.metadata, m, indent=2)

        return self.records


def crawl_from_config(config_path: str | Path) -> List[DocumentRecord]:
    crawler = Crawler(Path(config_path))
    return crawler.crawl()
