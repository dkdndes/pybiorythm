# PyBiorythm - Python Biorhythm Calculations

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-72%20passed-green.svg)](https://github.com/dkdndes/pybiorythm)
[![Coverage](https://img.shields.io/badge/coverage-90.33%25-brightgreen.svg)](https://github.com/dkdndes/pybiorythm)
[![CI/CD](https://github.com/dkdndes/pybiorythm/actions/workflows/ci.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](../LICENSE)

> **A modern Python library for biorhythm calculations with multiple output formats, comprehensive testing, and data analysis integration.**

!!! warning "Scientific Disclaimer"
    **Biorhythm theory is considered pseudoscience** with no scientific validity. This library is provided **for entertainment and educational purposes only**. Do not use for making important life decisions.

## Quick Start

### Installation
```bash
pip install biorythm
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

## Features

- **🎯 Multiple Output Formats**: ASCII charts (vertical/horizontal) and JSON data
- **📊 Data Analysis Ready**: JSON timeseries perfect for pandas, matplotlib, plotly
- **🔍 Critical Day Detection**: Identifies days when cycles cross zero  
- **⚙️ Configurable**: Adjustable chart width, time periods, and orientations
- **🧪 Well Tested**: 90%+ test coverage with comprehensive test suite
- **🐍 Modern Python**: Type hints, clean architecture, Python 3.9+

## Choose Your Documentation Path

### 🐍 **[Package Documentation](package/)**
**For Python developers using biorythm in applications**
- [Quick start guide](user-guide/quick-start/) and [installation](user-guide/installation/)
- [Complete API reference](api/) with examples
- [Usage examples](user-guide/usage-examples/) and patterns
- [CLI reference](user-guide/cli/) and configuration

### 📊 **[Data Analysis Examples](examples/)**
**For data scientists and analysts working with time series**
- Jupyter notebook examples and tutorials
- Pandas integration and data manipulation  
- Visualization with matplotlib, plotly, seaborn
- Statistical analysis and correlation studies

### 👨‍💻 **[GitHub Actions Patterns](github-actions/)**
**For developers learning CI/CD best practices**
- [GitHub Actions workflows](workflows/github-actions/) and templates
- [Security scanning](workflows/security/) and quality gates
- [Deployment strategies](workflows/blue-green/) and automation
- [Semantic versioning](workflows/semantic-versioning/) patterns

### 🚀 **[DevOps Learning Materials](devops/)**
**For DevOps specialists studying modern practices**
- [Development setup](developer-guide/setup/) and [architecture](developer-guide/architecture/)
- [Deployment guides](deployment/) for Docker and Kubernetes
- [Local testing](deployment/local-testing/) with GitHub Actions
- [Security practices](deployment/security/) and compliance

## Quick API Reference

```python
from biorythm import BiorhythmCalculator

# Initialize
calc = BiorhythmCalculator(width=55, days=29, orientation="vertical")

# Generate charts
calc.generate_chart(birthdate)                    # ASCII chart
data = calc.generate_timeseries_json(birthdate)   # JSON data

# Calculate values  
physical, emotional, intellectual = calc.calculate_biorhythm_values(birthdate, date)
```

**[→ Complete API Documentation](api/calculator/)**

---

**Note**: This documentation is organized by audience. Choose your path above based on whether you're using the Python package, analyzing data, learning CI/CD patterns, or studying DevOps practices! 🎯