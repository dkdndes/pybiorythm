# PyBiorythm - Educational GitHub Actions Showcase

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-72%20passed-green.svg)](https://github.com/dkdndes/pybiorythm)
[![Coverage](https://img.shields.io/badge/coverage-90.33%25-brightgreen.svg)](https://github.com/dkdndes/pybiorythm)
[![CI/CD](https://github.com/dkdndes/pybiorythm/actions/workflows/ci.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/docker-multi--stage-blue.svg)](Dockerfile)
[![Security](https://github.com/dkdndes/pybiorythm/actions/workflows/codeql.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/codeql.yml)
[![SBOM](https://github.com/dkdndes/pybiorythm/actions/workflows/sbom.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/sbom.yml)
[![Documentation](https://github.com/dkdndes/pybiorythm/actions/workflows/docs.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/docs.yml)
[![Semantic Release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

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

# Different chart orientations
python main.py -y 1990 -m 5 -d 15 --orientation horizontal --days 30

# Generate JSON output for data analysis
python main.py -y 1990 -m 5 -d 15 --orientation json-vertical
```

## Chart Types

### Vertical Chart (Traditional)
Time flows top-to-bottom, cycles displayed across width:
```
Mon May 15    p     :     e i    
Tue May 16       p  :  e      i  
Wed May 17          : p    e   i 
```

### Horizontal Chart (Timeline)
Time flows left-to-right, cycles displayed as wave patterns:
```
BIORHYTHM WAVE (all cycles)
                    e               
            p               i       
                        e           
```

### JSON Output
Structured data suitable for analysis, visualization, and testing.

## Features

- **Multiple Output Formats**: ASCII charts (vertical/horizontal) and JSON data
- **Critical Day Detection**: Identifies days when cycles cross zero
- **Cycle Information**: Shows when cycles repeat (644 days for physical+emotional, 21,252 days for all three)
- **Scientific Context**: Includes historical background and scientific disclaimers
- **Robust Error Handling**: Input validation and comprehensive error messages
- **Configurable Parameters**: Adjustable chart width, time periods, and orientations

## API Reference

### BiorhythmCalculator

Main class for generating biorhythm calculations and charts.

```python
BiorhythmCalculator(width=55, days=29, orientation="vertical")
```

**Parameters:**
- `width` (int): Chart width in characters (minimum 12)
- `days` (int): Number of days to plot
- `orientation` (str): "vertical" or "horizontal"

**Methods:**

#### `generate_chart(birthdate, plot_date=None)`
Generate and print ASCII chart to stdout.

#### `generate_timeseries_json(birthdate, plot_date=None, chart_orientation="vertical")`
Generate JSON payload with timeseries data and metadata.

#### `calculate_biorhythm_values(birthdate, target_date)`
Calculate raw cycle values for a specific date.

Returns tuple: `(physical, emotional, intellectual)` values between -1.0 and +1.0.

## Command Line Arguments

```
python main.py [OPTIONS]

Options:
  -y, --year YEAR              Birth year (1-9999)
  -m, --month MONTH            Birth month (1-12)  
  -d, --day DAY                Birth day (1-31)
  --orientation {vertical,horizontal,json-vertical,json-horizontal}
                               Chart orientation (default: vertical)
  --days DAYS                  Number of days to plot (default: 29)
  -h, --help                   Show help message
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

- **[📖 Complete Documentation](docs/README.md)** - Architecture, setup, and advanced features
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