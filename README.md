# PyBiorythm - Educational GitHub Actions Showcase

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-72%20passed-green.svg)](https://github.com/dkdndes/pybiorythm)
[![Coverage](https://img.shields.io/badge/coverage-90.33%25-brightgreen.svg)](https://github.com/dkdndes/pybiorythm)
[![CI/CD](https://github.com/dkdndes/pybiorythm/actions/workflows/ci.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> **Educational Note**: This project serves as a **comprehensive example of modern DevOps practices** and GitHub Actions workflows. While it implements biorhythm calculations (pseudoscience), its primary purpose is to demonstrate professional CI/CD pipelines, security practices, and deployment strategies.

## 🎓 What You'll Learn

This repository showcases **10 production-ready GitHub Actions workflows** that demonstrate:

- **Automated Testing & Quality Gates** - Multi-version Python testing, coverage enforcement, linting
- **Security-First Development** - CodeQL analysis, dependency scanning, SBOM generation
- **Multi-Environment Deployments** - Dev/staging/prod with blue-green deployment strategies  
- **Docker Multi-Architecture Builds** - ARM64/AMD64 container builds with security scanning
- **Semantic Release Automation** - Conventional commits driving automated versioning
- **Documentation Automation** - MkDocs deployment to GitHub Pages
- **Local Development Tools** - `act` for local GitHub Actions testing

## 🚀 Quick Start

### Installation

```bash
# Install the package
pip install biorythm

# Or install from source  
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm
pip install -e .
```

### Basic Usage

```python
from datetime import datetime
from biorythm import BiorhythmCalculator

# Create calculator
calc = BiorhythmCalculator(width=60, days=30)

# Generate chart for someone born May 15, 1990
birthdate = datetime(1990, 5, 15)
calc.generate_chart(birthdate)

# Generate JSON data for analysis
json_data = calc.generate_timeseries_json(birthdate)
```

### Command Line

```bash
# Interactive mode
python main.py

# Direct calculation  
python main.py -y 1990 -m 5 -d 15 --orientation vertical
python main.py -y 1990 -m 5 -d 15 --orientation json-horizontal
```

## 🔧 GitHub Actions Workflows (Educational Focus)

### Core CI/CD Pipeline (`ci.yml`)
**What it demonstrates:**
- **Matrix Testing** across Python 3.9-3.12
- **Quality Gates** with Ruff linting and 90%+ test coverage  
- **Security Scanning** with Bandit and Safety
- **Docker Testing** with multi-stage builds
- **Performance Benchmarking** with regression detection

```yaml
# Key features showcased:
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11', '3.12']
```

### Semantic Release Automation (`semantic-release.yml`)
**What it demonstrates:**
- **Conventional Commits** driving version bumps
- **Automated Changelog** generation
- **Git Tag Management** and GitHub releases
- **Cross-workflow Triggers** for downstream builds

### Multi-Environment Docker (`dev-docker.yml`, `docker-publish.yml`)
**What it demonstrates:**
- **Environment-specific Builds** (dev/staging/prod)
- **Semantic Versioning** for container tags
- **Multi-architecture Builds** (AMD64/ARM64)
- **Blue-green Deployment** manifest generation

### Security & Compliance (`codeql.yml`, `sbom.yml`)
**What it demonstrates:**
- **Static Code Analysis** with CodeQL
- **Software Bill of Materials** (BSI TR-03183-2-2 compliant)
- **Vulnerability Scanning** with Trivy
- **Security Attestation** and supply chain security

### Manual Deployment (`manual-deploy.yml`)
**What it demonstrates:**
- **Workflow Dispatch** with input parameters
- **Rolling vs Blue-Green** deployment strategies
- **Environment Gates** and approvals
- **Rollback Procedures** and traffic switching

### Documentation Automation (`docs.yml`)
**What it demonstrates:**
- **MkDocs** automated deployment to GitHub Pages
- **Link Validation** and content checking
- **Multi-environment** documentation builds
- **PR Preview** generation

## 🧪 Local Testing with `act`

This project includes comprehensive local testing tools:

```bash
# Quick development tests (30 seconds)
./local-test.sh quick

# Test specific workflow
./local-test.sh job test ci.yml

# List all available workflows
./local-test.sh list

# Validate workflow syntax
./local-test.sh validate
```

**Educational Value**: Learn how to test GitHub Actions locally before pushing to save time and CI credits.

## 📊 Quality Metrics & Monitoring

The project maintains enterprise-grade quality standards:

- ✅ **90.33% Test Coverage** (enforced at 85%+ minimum)
- ✅ **72 Passing Tests** across all components
- ✅ **Zero Security Vulnerabilities** (automated scanning)
- ✅ **BSI-Compliant SBOM** for supply chain transparency
- ✅ **Multi-architecture Docker** support (ARM64/AMD64)
- ✅ **Conventional Commits** with semantic versioning

## 🏗️ Architecture & Design Patterns

### DevOps Patterns Demonstrated

1. **GitFlow with Semantic Release**
   ```
   feature/* → develop → main → v1.2.3 (automated)
   ```

2. **Multi-Stage Docker Builds**
   ```dockerfile
   # Builder stage for dependencies
   FROM python:3.12-slim as builder
   # Production stage for runtime
   FROM python:3.12-slim as production
   ```

3. **Blue-Green Deployments**
   ```bash
   # Deploy to inactive slot
   kubectl apply -f deployment-blue.yaml
   # Switch traffic after validation  
   kubectl patch service app -p '{"spec":{"selector":{"slot":"blue"}}}'
   ```

4. **Security-First Development**
   - SBOM generation for all dependencies
   - Multi-layer vulnerability scanning
   - Signed container attestations
   - Automated security patch detection

## 📚 Documentation

For comprehensive documentation and advanced usage:

- **[📖 Complete Documentation](docs/)** - Architecture, setup, and advanced features
- **[🚀 Quick Start Guide](docs/user-guide/quick-start.md)** - Get started in 5 minutes
- **[⚙️ Developer Guide](docs/developer-guide/setup.md)** - Contributing and local development
- **[🚢 Deployment Guide](docs/deployment/)** - Docker, Kubernetes, and CI/CD
- **[🔧 GitHub Actions Guide](docs/workflows/)** - Understanding the CI/CD workflows

## 🔬 Scientific Disclaimer

**Important**: This software implements biorhythm theory, which is considered **pseudoscience**. Extensive scientific research has found **NO VALIDITY** to biorhythm theory beyond coincidence.

**This implementation is provided FOR EDUCATIONAL PURPOSES ONLY** to demonstrate:
- Modern Python packaging and distribution
- Comprehensive CI/CD pipeline implementation
- Security scanning and compliance practices
- Multi-environment deployment strategies
- Documentation automation

The biorhythm calculations serve as a simple, understandable domain for showcasing these DevOps practices.

## 🤝 Contributing

This project welcomes contributions that improve the **DevOps and CI/CD demonstrations**:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-workflow`)
3. **Follow** conventional commits (`feat: add new deployment strategy`)
4. **Test** locally with `act` before pushing
5. **Submit** a pull request

See [Contributing Guide](docs/developer-guide/contributing.md) for detailed guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🏷️ Keywords

`github-actions` `ci-cd` `devops` `docker` `python` `testing` `security` `automation` `deployment` `blue-green` `semantic-release` `sbom` `educational`

---

**Remember**: The real value here is in the **DevOps patterns and GitHub Actions workflows**, not the biorhythm calculations! 🎯