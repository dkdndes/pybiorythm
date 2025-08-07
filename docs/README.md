# PyBiorythm Documentation

Welcome to the comprehensive documentation for PyBiorythm - a Python library for biorhythm calculations and visualizations.

## 📚 Documentation Structure

### User Guide
- [Quick Start](user-guide/quick-start.md) - Get up and running quickly
- [Installation](user-guide/installation.md) - Installation options and requirements
- [Usage Examples](user-guide/usage-examples.md) - Common use cases and examples
- [Command Line Interface](user-guide/cli.md) - Command line reference
- [Output Formats](user-guide/output-formats.md) - Chart types and JSON output

### Developer Guide
- [Development Setup](developer-guide/setup.md) - Setting up development environment
- [Testing](developer-guide/testing.md) - Running tests and coverage
- [Code Quality](developer-guide/code-quality.md) - Linting, formatting, and standards
- [Contributing](developer-guide/contributing.md) - How to contribute to the project
- [Architecture](developer-guide/architecture.md) - Code structure and design

### API Reference
- [BiorhythmCalculator](api/calculator.md) - Main calculator class
- [Core Functions](api/core.md) - Core calculation functions
- [JSON Schema](api/json-schema.md) - JSON output format specification
- [Error Handling](api/errors.md) - Exception types and handling

### Deployment & DevOps
- [Deployment Guide](deployment/deployment-guide.md) - Complete deployment strategies
- [Docker Setup](deployment/docker.md) - Container deployment
- [Kubernetes](deployment/kubernetes.md) - K8s deployment manifests
- [Local Testing](deployment/local-testing.md) - Testing workflows locally
- [Security](deployment/security.md) - Security guidelines and SBOM

### Workflows & CI/CD
- [GitHub Actions](workflows/github-actions.md) - All workflow documentation
- [Semantic Versioning](workflows/semantic-versioning.md) - Version management
- [Blue-Green Deployment](workflows/blue-green.md) - Zero-downtime deployment
- [Security Scanning](workflows/security.md) - Security and vulnerability scanning

## 🚀 Quick Links

| Task | Documentation |
|------|---------------|
| **First time setup** | [Installation Guide](user-guide/installation.md) |
| **Basic usage** | [Quick Start](user-guide/quick-start.md) |
| **Command line** | [CLI Reference](user-guide/cli.md) |
| **Docker deployment** | [Docker Guide](deployment/docker.md) |
| **Development** | [Dev Setup](developer-guide/setup.md) |
| **Local GitHub Actions** | [act Testing](deployment/local-github-actions.md) |
| **API integration** | [API Reference](api/calculator.md) |

## 🔬 Scientific Disclaimer

**Important**: This software implements biorhythm theory, which is considered **pseudoscience**. Extensive scientific research has found **NO VALIDITY** to biorhythm theory beyond coincidence. This implementation is provided **FOR ENTERTAINMENT PURPOSES ONLY**.

## 📖 Viewing Documentation

### Option 1: MkDocs Server (Recommended)
```bash
# Install MkDocs
uv add --dev mkdocs mkdocs-material

# Serve documentation locally
uv run mkdocs serve

# View at http://127.0.0.1:8000
```

### Option 2: Static Files
All documentation is written in Markdown and can be viewed directly on GitHub or in any Markdown viewer.

### Option 3: GitHub Pages
The documentation is automatically deployed to GitHub Pages: [Documentation Site](https://dkdndes.github.io/pybiorythm/)

## 🔄 Keeping Documentation Updated

Documentation is automatically validated and updated through our CI/CD pipeline:
- ✅ **Link Validation**: All links are checked for validity
- ✅ **Code Examples**: Examples are tested in CI
- ✅ **Version Sync**: API docs are updated with releases
- ✅ **Screenshots**: Docker and deployment guides include current screenshots

## 📝 Contributing to Documentation

See [Contributing Guide](developer-guide/contributing.md#documentation) for information on improving the documentation.