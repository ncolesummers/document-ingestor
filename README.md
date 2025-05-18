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

### VS Code Tasks

Common development tasks are available via VS Code. Open the command palette and
run `Tasks: Run Task` to see the options. Provided tasks include:

- **Run Tests** – executes `uv run pytest -v`
- **Run Document Ingestor** – starts the CLI with `uv run document-ingestor`
- **Run Ruff** – lints the codebase with `uv run ruff .`
- **Run Mypy** – performs type checking with `uv run mypy src tests`
