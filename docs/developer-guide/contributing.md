# Contributing Guidelines

We welcome contributions to PyBiorythm! This document outlines the development process and standards.

**Project Maintainer**: Peter Rosemann (dkdndes@gmail.com)  
**GitHub**: [dkdndes](https://github.com/dkdndes)

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Set up** development environment (see [Development Setup](setup.md))
4. **Create** a feature branch from `develop`

```bash
git checkout develop
git checkout -b feature/your-feature-name
```

## Development Workflow

### 1. Development Setup
Follow the [Development Setup Guide](setup.md) to configure your environment with UV and all required dependencies.

### 2. Code Standards
- Follow [Code Quality Standards](code-quality.md)
- Write comprehensive tests (see [Testing Guide](testing.md))
- Use conventional commit messages
- Add type hints for all functions

### 3. Testing Requirements
```bash
# All tests must pass
uv run pytest

# Coverage must be ≥85%
uv run pytest --cov=. --cov-report=term-missing --cov-fail-under=85

# Code must pass linting
uv run ruff check .
uv run ruff format .
```

## Contribution Types

### Bug Fixes
- Create issue first describing the bug
- Reference issue in PR: `fixes #123`
- Include regression tests

### New Features
- Discuss in issue before implementation
- Update documentation
- Add comprehensive tests
- Follow existing patterns

### Documentation
- Use clear, concise language
- Include code examples
- Update relevant links
- Test documentation builds

## Commit Message Format

Use conventional commits:

```
type(scope): description

feat(calculator): add cycle repeat calculation
fix(cli): handle invalid date input gracefully  
docs(api): update calculator examples
test(core): add edge case coverage
```

## Pull Request Process

1. **Update** your branch with latest `develop`
2. **Test** locally with `act` if workflow changes
3. **Create** PR against `develop` branch
4. **Fill** PR template completely
5. **Respond** to review feedback promptly

### PR Requirements
- ✅ All CI checks pass
- ✅ Code coverage maintained (≥85%)
- ✅ Documentation updated
- ✅ Tests included for changes
- ✅ No merge conflicts

## Code Review Guidelines

### As a Reviewer
- Be constructive and respectful
- Focus on code quality, not coding style (automated)
- Check for test coverage
- Verify documentation updates

### As a Contributor  
- Address all feedback
- Ask questions if unclear
- Update PR description if scope changes
- Rebase/squash commits if requested

## Release Process

We use semantic versioning with automated releases:
- `develop` branch for ongoing development
- `main` branch for stable releases
- Tags created automatically via semantic-release

---

**Next Steps**: [Development Setup](setup.md) | [Code Quality](code-quality.md) | [Testing Guide](testing.md)