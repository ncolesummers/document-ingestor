# The 2025 Python developer's handbook: Best practices for Python 3.12+

Python development has evolved dramatically in recent years, with Python 3.12+ introducing significant improvements in performance, type annotations, and developer experience. This comprehensive guide covers essential best practices for modern Python development, from project structure to advanced tooling, helping you build robust, maintainable applications.

## The foundation: Modern project structure and organization

In modern Python development, proper project structure is crucial for maintainability and code organization. Two primary project layout structures exist, but the src layout has emerged as the industry standard for larger projects.

### Src layout vs flat layout

The **src layout** places your package inside a `src` directory, while the **flat layout** places it directly in the project root. The src layout provides several **significant advantages**:

```
# Recommended src layout
project_root/
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── module.py
├── tests/
├── pyproject.toml
└── README.md
```

This src layout prevents accidental imports of the development version and ensures testing against the installed package. It also provides cleaner imports and prevents accidental namespace pollution.

### Comprehensive project structure

For a complete Python 3.12+ project, follow this directory structure:

```
project_name/
├── .github/               # GitHub specific files
│   └── workflows/         # CI/CD configurations
├── src/                   # Source code package
│   └── package_name/      # Actual package (importable)
│       ├── __init__.py    # Package initialization
│       ├── py.typed       # Marker file for type checking
│       ├── main.py        # Main module
│       └── submodule/     # Subpackage
├── tests/                 # Test directory
│   ├── conftest.py        # pytest configuration
│   └── test_*.py          # Test modules
├── docs/                  # Documentation
├── examples/              # Example code
├── pyproject.toml         # Project configuration
└── README.md              # Project readme
```

### Modern configuration with pyproject.toml

Python 3.12+ projects should use `pyproject.toml` as their central configuration file:

```toml
[build-system]
requires = ["setuptools>=46.1.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "package_name"
version = "0.1.0"
description = "A short description of the project"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.12"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
dependencies = [
    "requests>=2.28.0",
    "numpy>=1.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.5",
]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 88
target-version = "py312"
select = ["E", "F", "I", "N", "W"]
```

## Package management using UV from Astral

UV is a modern, high-performance Python package manager written in Rust that provides **10-100x faster** dependency resolution and installation compared to traditional tools like pip or poetry.

### Installation

Install UV using the official install script:

```bash
# macOS/Linux
curl -fsSL https://astral.sh/uv/install.sh | bash

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Essential UV commands

UV combines functionality from pip, pip-tools, and virtualenv into a unified interface:

```bash
# Create a virtual environment
uv venv

# Create a virtual environment with specific Python version
uv venv --python 3.12

# Install a package
uv add requests

# Install a package with a specific version
uv add "requests>=2.30.0"

# Install development dependencies
uv add --dev pytest black mypy

# Synchronize the environment with dependencies
uv sync

# Run a Python script in the environment
uv run script.py

# Run a tool without installing it globally
uv tool run black .
# Or shorter form
uvx black .
```

### UV vs pip/poetry

UV offers several key advantages over traditional package managers:

1. **Speed**: 10-100x faster dependency resolution and installation
2. **Reliability**: Improved resolution algorithm with fewer conflicts
3. **Reproducibility**: Cross-platform lockfiles for consistent environments
4. **Feature set**: Combines pip, pip-tools, and virtualenv functionality
5. **Python management**: Built-in Python version management

### Project workflow with UV

A typical workflow for a new project with UV:

```bash
# Create project and initialize
mkdir myproject && cd myproject
uv init myproject
uv venv

# Add dependencies
uv add requests numpy
uv add --dev pytest black mypy

# Run development tasks
uv run pytest
uv run black src tests
```

## Code quality and style using Ruff

Ruff is an extremely fast Python linter and formatter written in Rust that replaces multiple tools (Flake8, Black, isort, etc.) while being **10-100x faster**.

### Installation and basic usage

```bash
# Using UV (recommended)
uv add --dev ruff

# Using pip
pip install ruff

# Basic usage
ruff check .           # Lint files
ruff format .          # Format files
ruff check --fix .     # Auto-fix linting issues
```

### Configuration with pyproject.toml

```toml
[tool.ruff]
# Enable Python 3.12 support
target-version = "py312"

# Set line length to 88 (same as Black default)
line-length = 88

# Exclude directories
exclude = [
    ".git",
    ".venv",
    "__pycache__",
]

# Enable autofix behavior
fix = true

[tool.ruff.lint]
# Enable specific rule sets
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "B",   # flake8-bugbear
    "I",   # isort
    "D",   # pydocstyle
]

# Configure pydocstyle to use Google-style docstrings
[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.format]
# Use double quotes for strings
quote-style = "double"

# Enable docstring code formatting
docstring-code-format = true
```

### IDE integration

For VS Code, install the Ruff extension and configure settings:

```json
{
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.fixAll.ruff": "explicit"
    },
    "ruff.lint.run": "onSave",
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff"
    }
}
```

### Common code smells detected by Ruff

Ruff can identify and often auto-fix common issues:

```python
# Unused imports (F401)
import os  # Error if not used

# Undefined names (F821)
print(undefined_variable)  # Error: undefined

# Mutable default arguments (B006)
def func(x=[]):  # Error: mutable default
    return x

# Unnecessary f-strings (F541)
x = f"No formatting here"  # Error: use regular string
```

## Documentation standards using Google-style docstrings

Google-style docstrings provide a clear, readable structure that is both human-friendly and machine-parseable.

### Docstring structure

A Google-style docstring typically consists of:
1. A one-line summary
2. An optional extended description
3. Sections for arguments, returns, raises, etc.

### Integration with type annotations

In Python 3.12+, use type annotations in function signatures while keeping docstrings focused on descriptions:

```python
def calculate_area(radius: float) -> float:
    """Calculate the area of a circle.
    
    Args:
        radius: The radius of the circle.
        
    Returns:
        The area of the circle.
    """
    return 3.14159 * radius ** 2
```

### Examples for different code elements

#### Module docstring

```python
"""Data processing utilities for handling CSV files.

This module provides functions to read, validate, transform, and write 
CSV data with a focus on performance and memory efficiency.

Typical usage example:
    data = read_csv('input.csv')
    transformed_data = transform_data(data)
    write_csv(transformed_data, 'output.csv')
"""

import csv
from typing import List, Dict, Any
```

#### Class docstring

```python
class DataProcessor:
    """A class for processing and transforming data.
    
    This class provides methods to load, validate, transform, and save
    data in various formats. It maintains state about the current data
    being processed and can be configured through various settings.
    
    Attributes:
        data: The data currently loaded in the processor.
        settings: Configuration settings for processing operations.
        is_modified: Whether the data has been modified since loading.
    """
    
    def __init__(self, settings: Dict[str, Any] = None) -> None:
        """Initialize the DataProcessor with optional settings.
        
        Args:
            settings: Configuration settings for the processor.
                If None, default settings will be used.
        """
        self.data = None
        self.settings = settings or {}
        self.is_modified = False
```

#### Method docstring

```python
def transform_data(self, transformation: str) -> bool:
    """Apply a transformation to the loaded data.
    
    Args:
        transformation: The name of the transformation to apply.
            Must be one of: 'normalize', 'standardize', 'log_scale'.
            
    Returns:
        True if the transformation was applied successfully, False otherwise.
        
    Raises:
        ValueError: If the transformation is not supported or if no data is loaded.
        
    Examples:
        >>> processor = DataProcessor()
        >>> processor.load_data([1, 2, 3, 4, 5])
        >>> processor.transform_data('normalize')
        True
    """
    if not self.data:
        raise ValueError("No data loaded")
    
    # Implementation
    return True
```

### Generating documentation

Use Sphinx with the Napoleon extension to generate HTML documentation from Google-style docstrings:

```python
# In docs/conf.py
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# Napoleon settings
napoleon_google_docstring = True
napoleon_include_init_with_doc = True
```

## Type annotations in Python 3.12+

Python 3.12+ introduces significant improvements to the typing system, making type annotations more concise and powerful.

### New type parameter syntax (PEP 695)

Python 3.12 introduced a new, more concise syntax for generic type parameters:

```python
# Python 3.12+ syntax
class Queue[T]:
    def __init__(self) -> None:
        self.elements: list[T] = []
    
    def push(self, element: T) -> None:
        self.elements.append(element)
    
    def pop(self) -> T:
        return self.elements.pop(0)

# Function with type parameters
def first[T](collection: list[T]) -> T:
    return collection[0]
```

### Type statement for aliases

Python 3.12 added a new `type` statement for creating type aliases:

```python
# Python 3.12+ syntax
type Vector = list[float]
type Point = tuple[float, float]
type CoordinateMap = dict[Point, Vector]

# Generic type aliases
type ListOrSet[T] = list[T] | set[T]
```

### Advanced typing concepts

#### Protocol classes (structural subtyping)

```python
from typing import Protocol

class Readable(Protocol):
    def read(self) -> str: ...

def process_data(source: Readable) -> str:
    return source.read()

# Any class with a read() method can be used
class DataFile:
    def read(self) -> str:
        return "data from file"

# Works because DataFile has a read() method
result = process_data(DataFile())
```

#### TypedDict for dictionary types

```python
from typing import TypedDict, NotRequired, Required, ReadOnly

# Basic TypedDict
class Movie(TypedDict):
    title: str
    year: int
    director: str

# TypedDict with optional fields
class FlexibleMovie(TypedDict, total=False):
    title: Required[str]  # Must be present
    year: Required[int]   # Must be present
    director: NotRequired[str]  # Optional
```

#### TypeGuard for type narrowing

```python
from typing import TypeGuard, Any

def is_string_list(val: list[Any]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process(items: list[Any]) -> None:
    if is_string_list(items):
        # items is now known to be list[str]
        for item in items:
            print(item.upper())  # Safe to call str methods
```

### Using type checkers

Two popular type checkers for Python are mypy and pyright:

```bash
# Install mypy
uv add --dev mypy

# Run mypy
mypy src/

# Configure mypy in pyproject.toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
```

## Testing approaches and frameworks

### pytest vs unittest comparison

pytest is generally recommended for new projects due to its simpler syntax and powerful features:

| Feature | pytest | unittest |
|---------|--------|------------|
| Syntax | Simple function-based | Class-based (more verbose) |
| Assertions | Standard Python assertions | Special assertion methods |
| Fixtures | Powerful, flexible fixtures | setUp/tearDown methods |
| Plugins | Rich ecosystem of plugins | Limited extensibility |
| Parameterization | Built-in parametrization | Limited support |

### Test organization

A typical test directory structure mirrors your application structure:

```
project/
├── src/
│   └── mypackage/
└── tests/
    ├── unit/
    │   ├── conftest.py
    │   └── test_module1.py
    ├── integration/
    │   └── test_integration.py
    └── functional/
        └── test_functional.py
```

### Using fixtures in pytest

Fixtures provide a way to set up and tear down test resources:

```python
# conftest.py
import pytest
from myapp.models import User
from myapp.database import Database

@pytest.fixture
def database():
    """Provide a clean database for each test."""
    db = Database(":memory:")
    yield db
    db.close()

@pytest.fixture
def user(database):
    """Create a test user."""
    user = User(name="Test User", email="test@example.com")
    database.save(user)
    return user

# test_user.py
def test_user_authentication(user, database):
    """Test user authentication with default password."""
    assert user.authenticate("default_password")
```

### Test parameterization

```python
import pytest

@pytest.mark.parametrize("input_value,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25),
])
def test_square(input_value, expected):
    """Test that the square function returns correct values."""
    assert input_value ** 2 == expected
```

### Property-based testing with Hypothesis

Hypothesis generates test cases to find edge cases automatically:

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sorting(numbers):
    """Test that sorting preserves elements and produces ordered results."""
    sorted_numbers = sorted(numbers)
    
    # Test that sorting preserves all elements
    assert set(sorted_numbers) == set(numbers)
    
    # Test that sorting produces a non-decreasing sequence
    assert all(sorted_numbers[i] <= sorted_numbers[i+1] 
               for i in range(len(sorted_numbers) - 1))
```

### Test coverage

Measure test coverage with pytest-cov:

```bash
# Generate coverage report in the terminal
pytest --cov=mypackage

# Generate HTML coverage report
pytest --cov=mypackage --cov-report=html
```

## CI/CD integration and workflow automation

### GitHub Actions for Python

#### Basic CI workflow

```yaml
# .github/workflows/python-tests.yml
name: Python Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: |
        pytest --cov=mypackage
```

#### Comprehensive CI pipeline

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"
    - name: Install uv
      run: curl -fsSL https://astral.sh/uv/install.sh | bash
    - name: Install dependencies and run lint
      run: |
        uv pip install ruff
        uv run ruff check .
        uv run ruff format --check .

  typecheck:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"
    - name: Install uv
      run: curl -fsSL https://astral.sh/uv/install.sh | bash
    - name: Install dependencies and run type check
      run: |
        uv pip install mypy
        uv pip install -e .
        uv run mypy src/

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
    # ... testing steps
```

### Packaging and deployment

Use GitHub Actions to automate package publishing:

```yaml
# .github/workflows/publish.yml
name: Publish Python Package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"
    - name: Install uv
      run: curl -fsSL https://astral.sh/uv/install.sh | bash
    - name: Install build tools
      run: uv pip install build twine
    - name: Build and publish
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        python -m build
        twine upload dist/*
```

## Docling integration for RAG systems

Docling is a powerful toolkit for document processing and conversion, making it ideal for RAG (Retrieval-Augmented Generation) systems.

### Understanding Docling architecture

Docling is built on two primary AI models:

1. **Layout Analysis Model**: Identifies and classifies blocks of text, images, tables, and other visual components
2. **TableFormer**: Transforms image-based tables into machine-readable formats

### RAG pipeline integration

```python
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_milvus import Milvus
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from pathlib import Path
import os

# Configure inputs
FILE_PATH = "https://example.com/document.pdf"
EMBED_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
GEN_MODEL_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# Load documents with Docling
loader = DoclingLoader(
    file_path=FILE_PATH,
    export_type="DOC_CHUNKS",
    chunker=HybridChunker(tokenizer=EMBED_MODEL_ID),
)
docs = loader.load()

# Create embeddings
embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL_ID)

# Set up vector store
milvus_uri = str(Path("./vector_db"))
vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=embedding,
    collection_name="docling_demo",
    connection_args={"uri": milvus_uri},
)

# Create retriever and LLM
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = HuggingFaceEndpoint(
    repo_id=GEN_MODEL_ID,
    task="text-generation",
)

# Create RAG chain
prompt = PromptTemplate.from_template(
    "Context information is below.\n---------------------\n{context}\n"
    "---------------------\nGiven the context information and not prior knowledge, "
    "answer the query.\nQuery: {input}\nAnswer:\n"
)
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Query the system
response = rag_chain.invoke({"input": "What is the main topic of this document?"})
```

### Document processing implementation

Here's an example implementation of a document processor with type annotations and Google-style docstrings:

```python
"""Document processing module for Docling-based RAG systems.

This module provides functionality for processing documents using Docling
and preparing them for ingestion into a RAG system.
"""

from pathlib import Path
from typing import List, Union, Optional, Dict, Any

from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from docling.datamodel.base_models import ConversionResult

class DocumentProcessor:
    """Document processor using Docling for RAG systems.
    
    This class handles the processing of documents using Docling, converting
    them into structured formats suitable for RAG systems.
    
    Attributes:
        converter: The Docling document converter instance.
        chunker: The chunker instance for splitting documents.
    """
    
    def __init__(
        self,
        chunker: Optional[HybridChunker] = None,
        artifacts_path: Optional[Path] = None,
    ) -> None:
        """Initialize the document processor.
        
        Args:
            chunker: Custom chunker for document splitting. If None, a default
                chunker will be used.
            artifacts_path: Path to the Docling artifacts. If None, the default
                path will be used.
        """
        self.converter = DocumentConverter(artifacts_path=artifacts_path)
        self.chunker = chunker or HybridChunker()
    
    def process_document(
        self,
        source: Union[str, Path],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversionResult:
        """Process a document using Docling.
        
        Args:
            source: The document source, either a local path or a URL.
            metadata: Optional metadata to attach to the document.
            
        Returns:
            A ConversionResult object containing the processed document.
            
        Raises:
            ValueError: If the document cannot be processed.
        """
        try:
            result = self.converter.convert(source)
            
            # Add metadata if provided
            if metadata and result.document:
                result.document.metadata = {
                    **(result.document.metadata or {}),
                    **metadata,
                }
                
            return result
        except Exception as e:
            raise ValueError(f"Failed to process document: {e}") from e
```

### Chunking strategies

Effective chunking is critical for RAG systems. Docling provides several approaches:

```python
from docling.chunking import HybridChunker
from langchain_docling import DoclingLoader

# Configure a hybrid chunker with specific parameters
chunker = HybridChunker(
    chunk_size=1024,
    chunk_overlap=100,
    tokenizer="sentence-transformers/all-MiniLM-L6-v2",
)

# Use the chunker with DoclingLoader
loader = DoclingLoader(
    file_path="https://example.com/document.pdf",
    export_type="DOC_CHUNKS",
    chunker=chunker,
)
```

## Putting it all together: A complete example

Here's a complete project that demonstrates all the best practices covered in this guide:

```python
"""
Example package showcasing modern Python 3.12+ best practices.

This module serves as the entry point for the example package.
"""

from typing import Dict, List, Optional, Union
import argparse

from example_package.processor import DataProcessor
from example_package.config import Settings


def process_files(
    file_paths: List[str], 
    config_path: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Dict[str, Union[int, float, str]]]:
    """Process multiple files according to configuration.
    
    Args:
        file_paths: List of paths to files that should be processed.
        config_path: Optional path to configuration file. If not provided,
            default configuration will be used.
        verbose: Whether to print verbose output during processing.
        
    Returns:
        Dictionary mapping file paths to their processing results.
        
    Raises:
        FileNotFoundError: If any of the input files cannot be found.
        ValueError: If the configuration file is invalid.
    """
    # Load settings
    settings = Settings.from_file(config_path) if config_path else Settings()
    
    # Create processor
    processor = DataProcessor(settings=settings, verbose=verbose)
    
    # Process each file
    results = {}
    for file_path in file_paths:
        if verbose:
            print(f"Processing {file_path}...")
        result = processor.process_file(file_path)
        results[file_path] = result
    
    return results


def main() -> None:
    """Main entry point for the command line interface."""
    parser = argparse.ArgumentParser(description="Process files using example package")
    parser.add_argument(
        "files", 
        nargs="+", 
        help="Paths to files that should be processed"
    )
    parser.add_argument(
        "--config", 
        "-c",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--verbose", 
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        results = process_files(
            file_paths=args.files,
            config_path=args.config,
            verbose=args.verbose
        )
        
        # Print results
        for file_path, result in results.items():
            print(f"Results for {file_path}:")
            for key, value in result.items():
                print(f"  {key}: {value}")
    
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
```

## Conclusion 

Modern Python development with Python 3.12+ offers significant improvements in developer experience, code quality, and performance. By adopting the best practices outlined in this guide – src layout, UV package management, Ruff for linting, comprehensive type annotations, proper testing, and CI/CD automation – you'll build more maintainable, robust, and efficient Python applications.

The Python ecosystem continues to evolve rapidly, with tools like UV and Ruff representing a new generation of developer tools that emphasize performance and developer experience. By leveraging these tools alongside Python's improved typing system, you can write code that is both easier to understand and more reliable.

Remember that these best practices are not just about following conventions – they solve real problems and make your development process more efficient. Adopt them incrementally and enjoy the benefits of modern Python development.