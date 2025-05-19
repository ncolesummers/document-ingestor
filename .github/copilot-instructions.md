# Agent Instructions

- Use [uv](https://github.com/astral-sh/uv) for package management.
- When adding dependencies to this project, prefer `uv add <package>` instead of `uv pip install`. `uv add` updates `pyproject.toml` automatically and ensures that all dependencies are tracked.
- Reserve `uv pip install` for temporary, one-off installations during development.
- Tests can be run using `uv run pytest` or `uv run pytest -v` for verbose output.
