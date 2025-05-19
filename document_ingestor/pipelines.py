# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from __future__ import annotations

import uuid
from datetime import datetime
from io import BytesIO
from pathlib import Path

import requests
from docling.document_converter import DocumentConverter
from itemadapter import ItemAdapter
from w3lib.html import remove_tags


class DocumentIngestorPipeline:
    """Clean scraped pages and persist them as text files."""

    def __init__(self) -> None:
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.converter = DocumentConverter()

    def _sanitize_filename(self, name: str) -> str:
        safe = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in name)
        safe = safe.strip().replace(" ", "_")
        return safe[:50] if safe else "document"

    def _extract_pdf_text(self, url: str, body: bytes | str | None) -> str:
        try:
            if isinstance(body, (bytes, bytearray)):
                source = BytesIO(body)
            else:
                source = url

            result = self.converter.convert(source)

            doc = getattr(result, "document", result)
            if hasattr(doc, "text"):
                return doc.text
            if hasattr(doc, "to_text"):
                return doc.to_text()
            return str(doc)
        except Exception as exc:  # noqa: BLE001
            # Log and return empty string on failure
            print(f"Failed to extract PDF from {url}: {exc}")
            return ""

    def process_item(self, item: dict, spider):
        adapter = ItemAdapter(item)

        url = adapter.get("url")
        title = adapter.get("title") or url or "document"
        body = adapter.get("body")

        if url and url.lower().endswith(".pdf"):
            text = self._extract_pdf_text(url, body)
        else:
            html = body.decode("utf-8", "ignore") if isinstance(body, (bytes, bytearray)) else str(body)
            text = remove_tags(html)

        adapter["body_text"] = text.strip()
        adapter["source"] = spider.name
        adapter["retrieved_at"] = datetime.utcnow().isoformat()

        filename = f"{self._sanitize_filename(title)}_{uuid.uuid4().hex[:8]}.txt"
        filepath = self.output_dir / filename
        filepath.write_text(adapter["body_text"], encoding="utf-8")

        if "body" in adapter:
            del adapter["body"]

        return item
