# Development Setup

This guide will help you set up a development environment for contributing to PyBiorythm.

## Prerequisites

- **Python 3.8+** (3.12 recommended)
- **Git** for version control
- **uv** package manager (recommended) or pip
- **Docker** (optional, for container testing)

## Quick Setup

### Option 1: uv (Recommended)

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm

# Install with all development dependencies
uv sync --group dev

# Install with documentation dependencies too
uv sync --group dev --group docs

# Activate virtual environment (if needed)
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

### Option 2: pip + venv

```bash
# Clone repository
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install development dependencies
pip install -e ".[dev]"
```

## Development Dependencies

The project includes comprehensive development tools:

### Testing & Quality
- **pytest**: Testing framework with fixtures and parametrization
- **pytest-cov**: Code coverage reporting and enforcement
- **pytest-benchmark**: Performance testing and regression detection
- **ruff**: Fast Python linter and code formatter
- **bandit**: Security vulnerability scanner
- **safety**: Dependency vulnerability checker

### Build & Release
- **build**: Modern Python package building
- **twine**: Secure PyPI package publishing
- **python-semantic-release**: Automated versioning and changelog

### Documentation
- **mkdocs**: Static site generator for documentation
- **mkdocs-material**: Material Design theme
- **mkdocs-mermaid2-plugin**: Diagram support

### Security & Compliance
- **cyclonedx-bom**: Software Bill of Materials generation

## Verify Installation

Run the development checks to ensure everything is working:

```bash
# Run all tests
uv run pytest

# Check test coverage
uv run pytest --cov=. --cov-report=term-missing

# Run linting
uv run ruff check .

# Run formatting check
uv run ruff format --check .

# Security scan
uv run bandit -r biorythm/

# Dependency vulnerability check
uv run safety check
```

All checks should pass:
```
✅ 72 tests passed
✅ 90%+ coverage
✅ No linting issues
✅ Code properly formatted
✅ No security issues
✅ No vulnerable dependencies
```

## Development Workflow

### 1. Create Feature Branch

```bash
# Create and switch to feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b bugfix/issue-description
```

### 2. Make Changes

Edit code following the project conventions:

- **Code Style**: Follows ruff formatting standards
- **Type Hints**: Use type hints for function parameters and returns
- **Docstrings**: Document all public functions and classes
- **Testing**: Add tests for new functionality

### 3. Run Development Checks

```bash
# Auto-format code
uv run ruff format .

# Fix linting issues
uv run ruff check . --fix

# Run tests with coverage
uv run pytest --cov=. --cov-fail-under=85

# Generate coverage report
uv run pytest --cov=. --cov-report=html
# View in htmlcov/index.html
```

### 4. Commit Changes

Use conventional commit format:

```bash
# Feature commits
git commit -m "feat: add horizontal chart orientation"

# Bug fix commits  
git commit -m "fix: resolve date validation edge case"

# Documentation commits
git commit -m "docs: update API documentation"

# Test commits
git commit -m "test: add edge case tests for date handling"
```

### 5. Push and Create PR

```bash
# Push feature branch
git push origin feature/your-feature-name

# Create pull request via GitHub CLI (if installed)
gh pr create --title "feat: add horizontal chart orientation" --body "Description of changes"
```

## Testing Guidelines

### Test Structure

```
tests/
├── conftest.py                   # Shared fixtures
├── test_biorhythm_calculator.py  # Core functionality tests
├── test_main.py                  # CLI interface tests  
├── test_json_timeseries.py       # JSON output tests
└── test_coverage_gaps.py         # Edge case coverage
```

### Writing Tests

```python
import pytest
from datetime import datetime
from biorythm import BiorhythmCalculator

class TestNewFeature:
    def test_basic_functionality(self):
        """Test basic feature behavior"""
        calc = BiorhythmCalculator()
        result = calc.some_method()
        assert result is not None
    
    def test_edge_case(self):
        """Test edge case handling"""
        calc = BiorhythmCalculator()
        with pytest.raises(ValueError):
            calc.some_method(invalid_input)
    
    @pytest.mark.parametrize("input,expected", [
        (datetime(1990, 5, 15), "expected_output"),
        (datetime(2000, 1, 1), "other_output"),
    ])
    def test_multiple_inputs(self, input, expected):
        """Test with multiple input values"""
        calc = BiorhythmCalculator()
        result = calc.some_method(input)
        assert result == expected
```

### Running Specific Tests

```bash
# Run specific test file
uv run pytest tests/test_biorhythm_calculator.py

# Run specific test class
uv run pytest tests/test_biorhythm_calculator.py::TestBiorhythmCalculator

# Run specific test method
uv run pytest tests/test_main.py::TestMainFunction::test_interactive_mode

# Run tests matching pattern
uv run pytest -k "json" -v

# Run only fast tests (exclude slow benchmarks)
uv run pytest -m "not slow"
```

## Code Quality Standards

### Linting Configuration

The project uses ruff with the following rules:

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py38"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings  
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Type Checking

While not enforced, type hints are encouraged:

```python
from typing import Optional, Tuple
from datetime import datetime

def calculate_cycles(
    birthdate: datetime, 
    target_date: Optional[datetime] = None
) -> Tuple[float, float, float]:
    """Calculate biorhythm cycles with type hints"""
    # Implementation
    return physical, emotional, intellectual
```

## Docker Development

### Development Container

```bash
# Build development image
docker build --target builder -t biorythm:dev .

# Run with volume mount for live editing
docker run -v $(pwd):/app -it biorythm:dev bash

# Run tests in container
docker run -v $(pwd):/app biorythm:dev pytest
```

### Multi-Architecture Testing

```bash
# Build for both AMD64 and ARM64
docker buildx build --platform linux/amd64,linux/arm64 -t biorythm:multi .

# Test on specific architecture
docker run --platform linux/amd64 biorythm:multi python -m pytest
```

## Documentation Development

### Serve Documentation Locally

```bash
# Install docs dependencies
uv sync --group docs

# Serve documentation with hot reload
uv run mkdocs serve

# View at http://127.0.0.1:8000
```

### Building Documentation

```bash
# Build static site
uv run mkdocs build

# Deploy to GitHub Pages
uv run mkdocs gh-deploy
```

## Troubleshooting

### Common Issues

#### uv not found
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart terminal or source ~/.bashrc
```

#### Permission denied (pytest)
```bash
# Ensure virtual environment is activated
source .venv/bin/activate
# Or use uv run prefix
uv run pytest
```

#### Import errors
```bash
# Install project in editable mode
uv pip install -e .
```

### Getting Help

- **Documentation**: This site and inline code comments
- **Issues**: [GitHub Issues](https://github.com/dkdndes/pybiorythm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dkdndes/pybiorythm/discussions)

## Next Steps

- **Read**: [Testing Guide](testing.md)
- **Review**: [Code Quality Standards](code-quality.md)
- **Contribute**: [Contributing Guidelines](contributing.md)
- **Architecture**: [Project Architecture](architecture.md)