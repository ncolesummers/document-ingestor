"""
Script to download static resources (recommended_crawl_depth == 0) listed in docs/resources.jsonl.

Usage:
    python download_static_resources.py --resources docs/resources.jsonl --output static_resources
"""

import json
import os
import argparse
from pathlib import Path
from urllib.parse import urlparse, unquote
import urllib.request


def sanitize_filename(name: str) -> str:
    # Replace unsafe characters
    return (
        "".join(c if c.isalnum() or c in (" ", ".", "_", "-") else "_" for c in name)
        .strip()
        .replace(" ", "_")
    )


def download_resources(resources_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    with resources_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line}")
                continue

            if entry.get("recommended_crawl_depth") == 0:
                url = entry.get("url")
                if not url:
                    continue
                # Determine filename
                parsed = urlparse(url)
                name = Path(unquote(parsed.path)).name
                if not name:
                    # fallback to title
                    title = entry.get("title", "resource")
                    name = sanitize_filename(title)
                # ensure proper extension
                filepath = output_dir / name
                if filepath.exists():
                    print(f"Already downloaded: {name}")
                    continue
                print(f"Downloading {url} -> {name}")
                try:
                    urllib.request.urlretrieve(url, filepath)
                except Exception as e:
                    print(f"Failed to download {url}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Download static resources from resources.jsonl"
    )
    parser.add_argument(
        "--resources",
        type=Path,
        default=Path("docs/resources.jsonl"),
        help="Path to resources.jsonl",
    )
    parser.add_argument(
        "--output", type=Path, default=Path("static_resources"), help="Output directory"
    )
    args = parser.parse_args()
    download_resources(args.resources, args.output)


if __name__ == "__main__":
    main()
