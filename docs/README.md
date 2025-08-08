# PyBiorythm Documentation

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-72%20passed-green.svg)](https://github.com/dkdndes/pybiorythm)
[![Coverage](https://img.shields.io/badge/coverage-90.33%25-brightgreen.svg)](https://github.com/dkdndes/pybiorythm)
[![CI/CD](https://github.com/dkdndes/pybiorythm/actions/workflows/ci.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/docker-multi--stage-blue.svg)](../Dockerfile)
[![Security](https://github.com/dkdndes/pybiorythm/actions/workflows/codeql.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/codeql.yml)
[![SBOM](https://github.com/dkdndes/pybiorythm/actions/workflows/sbom.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/sbom.yml)
[![Documentation](https://github.com/dkdndes/pybiorythm/actions/workflows/docs.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/docs.yml)
[![Semantic Release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](../LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Welcome to PyBiorythm - a comprehensive Python library for generating biorhythm charts and timeseries data.

!!! warning "Scientific Disclaimer"
    **This software implements biorhythm theory, which is considered PSEUDOSCIENCE.** Extensive scientific research has found NO VALIDITY to biorhythm theory beyond coincidence. Multiple controlled studies have consistently failed to find any correlation between the proposed 23, 28, and 33-day cycles and human performance or life events.

    **This implementation is provided FOR ENTERTAINMENT PURPOSES ONLY** and should NOT be used for making any important life decisions.

## What is PyBiorythm?

PyBiorythm is a modern Python library that implements the classical biorhythm theory with multiple output formats, comprehensive testing, and enterprise-grade CI/CD pipelines. It's designed for educational purposes, data analysis experiments, and entertainment applications.

### Key Features

**🎯 Multiple Output Formats**
- **ASCII Charts**: Traditional vertical and horizontal biorhythm charts
- **JSON Data**: Structured timeseries data for analysis and visualization
- **Configurable Parameters**: Adjustable chart width, time periods, and orientations

**👨‍💻 Developer Friendly**
- **90.33% Test Coverage** with comprehensive test suite
- **Modern Python**: Type hints, dataclasses, and clean architecture
- **Docker Support**: Multi-stage builds for production deployment
- **CI/CD Ready**: GitHub Actions workflows for quality assurance

**📊 Data Analysis Ready**
- **JSON Timeseries**: Perfect for pandas, matplotlib, and data science workflows
- **Critical Day Detection**: Identifies when cycles cross zero
- **Statistical Properties**: Comprehensive metadata for analysis
- **Feature Engineering**: Ready for machine learning experiments

## Quick Start

### Installation

**With pip (recommended):**
```bash
# Install from PyPI (when published)
pip install biorythm

# Or install from source
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm
pip install .
```

**With uv (fastest):**
```bash
# Using uv package manager
uv add biorythm

# Or from source with uv
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm
uv pip install -e .
```

**With Docker (easiest):**
```bash
# Using Docker
docker run -it biorythm:latest

# Or build locally
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm
docker build -t biorythm:latest .
docker run -it biorythm:latest
```

See the [Quick Start Guide](user-guide/quick-start.md) for detailed usage instructions and examples.

## Documentation Structure

### 🚀 User Guide
Get started quickly with installation, usage examples, and CLI reference.
- **[Quick Start Guide](user-guide/quick-start.md)** - Get up and running in 5 minutes
- **[Installation Guide](user-guide/installation.md)** - Multiple installation methods
- **[CLI Reference](user-guide/cli.md)** - Command line interface documentation
- **[Usage Examples](user-guide/usage-examples.md)** - Practical examples and use cases
- **[Output Formats](user-guide/output-formats.md)** - Chart types and JSON formats

### 💻 API Reference
Comprehensive API documentation for the BiorhythmCalculator class and core functions.
- **[Calculator API](api/calculator.md)** - Main BiorhythmCalculator class
- **[Core Functions](api/core.md)** - Low-level calculation functions
- **[JSON Schema](api/json-schema.md)** - Complete JSON output specification
- **[Error Handling](api/errors.md)** - Exception types and error handling

### 🛠 Developer Guide
Development setup, testing, code quality, and contribution guidelines.
- **[Development Setup](developer-guide/setup.md)** - Environment configuration
- **[Architecture](developer-guide/architecture.md)** - Project structure and design
- **[Testing Guide](developer-guide/testing.md)** - Testing framework and coverage
- **[Code Quality](developer-guide/code-quality.md)** - Linting, formatting, and standards
- **[Contributing](developer-guide/contributing.md)** - How to contribute to the project

### 🚢 Deployment
Docker deployment, Kubernetes manifests, and production deployment strategies.
- **[Deployment Guide](deployment/deployment-guide.md)** - Production deployment strategies
- **[Docker Setup](deployment/docker.md)** - Container deployment
- **[Kubernetes](deployment/kubernetes.md)** - Cluster deployment with manifests
- **[Security & Compliance](deployment/security.md)** - Security best practices
- **[Local GitHub Actions](deployment/local-github-actions.md)** - Testing workflows locally

## Chart Examples

For chart examples and detailed output format documentation, see:
- [Output Formats Guide](user-guide/output-formats.md) - All chart types and formats
- [Usage Examples](user-guide/usage-examples.md) - Practical use cases 
- [JSON Schema](api/json-schema.md) - Complete JSON structure reference

## What's Next?

- **New Users**: Start with the [Quick Start Guide](user-guide/quick-start.md)
- **Developers**: Check out the [Development Setup](developer-guide/setup.md) and [Architecture Overview](developer-guide/architecture.md)
- **Contributors**: Review the [Code Quality Standards](developer-guide/code-quality.md) and [Contributing Guidelines](developer-guide/contributing.md)
- **Data Scientists**: Explore the [JSON Schema](api/json-schema.md) and [Output Formats](user-guide/output-formats.md)
- **DevOps**: Review the [Deployment Guide](deployment/deployment-guide.md) and [Security Best Practices](deployment/security.md)

## Version Information

**Current Version**: 1.2.1  
**Python Compatibility**: 3.9+  
**License**: MIT  
**Author**: Peter Rosemann (dkdndes@gmail.com)  
**Repository**: [GitHub](https://github.com/dkdndes/pybiorythm)