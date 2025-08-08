# Code Quality Standards

PyBiorythm maintains high code quality through comprehensive linting, testing, and automated checks.

**Maintained by**: Peter Rosemann (dkdndes@gmail.com)

## Code Quality Tools

### Ruff (Linting & Formatting)
- **Linting**: `uv run ruff check .`
- **Formatting**: `uv run ruff format .`
- Configuration in `pyproject.toml`

### Test Coverage
- **Minimum**: 85% coverage enforced
- **Current**: 90%+ coverage maintained
- **Command**: `uv run pytest --cov=. --cov-report=term-missing`

### Type Checking
- Python type hints used throughout codebase
- Static analysis via CI/CD pipeline

## Quality Gates

All code must pass:
- ✅ Ruff linting (no errors)
- ✅ Ruff formatting compliance
- ✅ 85%+ test coverage
- ✅ All tests passing
- ✅ Security scans (bandit, safety)

## Pre-commit Standards

Before committing code:

```bash
# Run quality checks
uv run ruff check .
uv run ruff format .
uv run pytest --cov=. --cov-report=term-missing --cov-fail-under=85
uv run safety check
uv run bandit -r biorythm/ main.py
```

---

**Related**: [Testing Guide](testing.md) | [Development Setup](setup.md) | [Contributing Guidelines](contributing.md)