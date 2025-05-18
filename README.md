# document-ingestor

A document ingestion pipeline for use with RAG-based workflows.

This project follows the `src` layout recommended in the documentation. All code
lives under `src/document_ingestor` and tests are in `tests`.

## Development

Install dependencies using [uv](https://github.com/astral-sh/uv):

```bash
uv venv
uv sync
```

Run the command-line interface:

```bash
uv run document-ingestor
```

Run tests:

```bash
uv run pytest
```
