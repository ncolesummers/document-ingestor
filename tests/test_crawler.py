from __future__ import annotations

import json
from pathlib import Path
from document_ingestor import Crawler

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class TestServer:
    def __init__(self, responses: list[tuple[int, bytes, dict[str, str]]]):
        self.responses = responses
        self.httpd: ThreadingHTTPServer | None = None
        self.thread: threading.Thread | None = None

    def __enter__(self) -> str:
        responses_iter = iter(self.responses)

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # type: ignore[override]
                try:
                    status, body, headers = next(responses_iter)
                except StopIteration:  # pragma: no cover - unexpected
                    status, body, headers = 500, b"", {}
                self.send_response(status)
                for k, v in headers.items():
                    self.send_header(k, v)
                self.end_headers()
                if body:
                    self.wfile.write(body)

        self.httpd = ThreadingHTTPServer(("localhost", 0), Handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        return f"http://localhost:{self.httpd.server_address[1]}"

    def __exit__(self, exc_type, exc, tb) -> None:
        assert self.httpd and self.thread  # for mypy
        self.httpd.shutdown()
        self.thread.join()


def test_crawl_fetches_and_stores(tmp_path: Path) -> None:
    responses = [
        (200, b"hello", {"ETag": "abc", "Last-Modified": "date"}),
    ]
    with TestServer(responses) as base_url:
        config = {
            "seed_urls": [f"{base_url}/doc"],
            "output_dir": str(tmp_path / "out"),
            "metadata_path": str(tmp_path / "meta.json"),
        }
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps(config))

        crawler = Crawler(config_path)
        results = crawler.crawl()

    assert len(results) == 1
    rec = results[0]
    assert rec.url == f"{base_url}/doc"
    output_file = Path(rec.path)
    assert output_file.exists()
    assert output_file.read_bytes() == b"hello"
    meta = json.loads((tmp_path / "meta.json").read_text())
    assert meta[f"{base_url}/doc"]["etag"] == "abc"


def test_crawl_skips_on_304(tmp_path: Path) -> None:
    meta_path = tmp_path / "meta.json"
    out_dir = tmp_path / "out"
    responses = [
        (200, b"hello", {"ETag": "abc"}),
        (304, b"", {}),
    ]
    with TestServer(responses) as base_url:
        config = {
            "seed_urls": [f"{base_url}/doc"],
            "output_dir": str(out_dir),
            "metadata_path": str(meta_path),
        }
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps(config))

        crawler = Crawler(config_path)
        crawler.crawl()

        crawler = Crawler(config_path)
        results = crawler.crawl()

    assert results[0].status == "skipped"
    # file should still exist with original content
    files = list(out_dir.iterdir())
    assert files and files[0].read_bytes() == b"hello"
