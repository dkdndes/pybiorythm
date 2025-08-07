# PyBiorythm Documentation

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-72%20passed-green.svg)](https://github.com/dkdndes/pybiorythm)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)](https://github.com/dkdndes/pybiorythm)
[![CI/CD](https://github.com/dkdndes/pybiorythm/actions/workflows/ci.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/docker-multi--stage-blue.svg)](Dockerfile)
[![Security](https://github.com/dkdndes/pybiorythm/actions/workflows/codeql.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/codeql.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Welcome to PyBiorythm - a comprehensive Python library for generating biorhythm charts and timeseries data.

!!! warning "Scientific Disclaimer"
    **This software implements biorhythm theory, which is considered PSEUDOSCIENCE.** Extensive scientific research has found NO VALIDITY to biorhythm theory beyond coincidence. Multiple controlled studies have consistently failed to find any correlation between the proposed 23, 28, and 33-day cycles and human performance or life events.

    **This implementation is provided FOR ENTERTAINMENT PURPOSES ONLY** and should NOT be used for making any important life decisions.

## What is PyBiorythm?

PyBiorythm is a modern Python library that implements the classical biorhythm theory with multiple output formats, comprehensive testing, and enterprise-grade CI/CD pipelines. It's designed for educational purposes, data analysis experiments, and entertainment applications.

### Key Features

=== "Multiple Output Formats"
    - **ASCII Charts**: Traditional vertical and horizontal biorhythm charts
    - **JSON Data**: Structured timeseries data for analysis and visualization
    - **Configurable Parameters**: Adjustable chart width, time periods, and orientations

=== "Developer Friendly"
    - **90% Test Coverage** with comprehensive test suite
    - **Modern Python**: Type hints, dataclasses, and clean architecture
    - **Docker Support**: Multi-stage builds for production deployment
    - **CI/CD Ready**: GitHub Actions workflows for quality assurance

=== "Data Analysis Ready"
    - **JSON Timeseries**: Perfect for pandas, matplotlib, and data science workflows
    - **Critical Day Detection**: Identifies when cycles cross zero
    - **Statistical Properties**: Comprehensive metadata for analysis
    - **Feature Engineering**: Ready for machine learning experiments

## Quick Start

### Installation

```bash tab="pip"
# Install from PyPI (when published)
pip install biorythm

# Or install from source
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm
pip install .
```

```bash tab="uv"
# Using uv (recommended)
uv add biorythm

# Or from source with uv
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm
uv pip install -e .
```

```bash tab="Docker"
# Using Docker (easiest)
docker run -it biorythm:latest

# Or build locally
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm
docker build -t biorythm:latest .
docker run -it biorythm:latest
```

### Basic Usage

```python
from datetime import datetime
from biorythm import BiorhythmCalculator

# Create calculator instance
calc = BiorhythmCalculator(width=60, days=30, orientation="vertical")

# Generate chart for someone born May 15, 1990
birthdate = datetime(1990, 5, 15)
calc.generate_chart(birthdate)

# Generate JSON timeseries data
json_data = calc.generate_timeseries_json(birthdate)
print(json_data)
```

### Command Line Usage

```bash
# Interactive mode
python main.py

# Command line with arguments
python main.py -y 1990 -m 5 -d 15

# Different chart orientations
python main.py -y 1990 -m 5 -d 15 --orientation horizontal
python main.py -y 1990 -m 5 -d 15 --orientation json-vertical
```

## Documentation Structure

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } __User Guide__

    ---

    Get started quickly with installation, usage examples, and CLI reference.

    [:octicons-arrow-right-24: User Guide](user-guide/quick-start.md)

-   :material-code-braces:{ .lg .middle } __API Reference__

    ---

    Comprehensive API documentation for the BiorhythmCalculator class and core functions.

    [:octicons-arrow-right-24: API Reference](api/calculator.md)

-   :material-tools:{ .lg .middle } __Developer Guide__

    ---

    Development setup, testing, code quality, and contribution guidelines.

    [:octicons-arrow-right-24: Developer Guide](developer-guide/setup.md)

-   :material-cloud-upload:{ .lg .middle } __Deployment__

    ---

    Docker deployment, Kubernetes manifests, and production deployment strategies.

    [:octicons-arrow-right-24: Deployment](deployment/deployment-guide.md)

</div>

## Chart Examples

### Vertical Chart (Traditional)
```
Mon May 15    p     :     e i    
Tue May 16       p  :  e      i  
Wed May 17          : p    e   i 
Thu May 18          :   p     e i
Fri May 19          :      p e  i
```

### Horizontal Chart (Timeline)
```
BIORHYTHM WAVE (all cycles)
                    e               
            p               i       
                        e           
```

### JSON Output Structure

```json
{
  "meta": {
    "generator": "biorythm",
    "version": "1.2.1",
    "birthdate": "1990-05-15",
    "plot_date": "2025-08-07",
    "days_alive": 12837,
    "cycle_lengths_days": {
      "physical": 23,
      "emotional": 28,
      "intellectual": 33
    }
  },
  "data": [
    {
      "date": "2025-07-24",
      "physical": -0.8987940462991669,
      "emotional": 0.9744583088414919,
      "intellectual": -0.9510565162951536
    }
  ]
}
```

## What's Next?

- **New Users**: Start with the [Quick Start Guide](user-guide/quick-start.md)
- **Developers**: Check out the [Development Setup](developer-guide/setup.md)
- **Data Scientists**: Explore the [JSON Schema](api/json-schema.md)
- **DevOps**: Review the [Deployment Guide](deployment/deployment-guide.md)

## Version Information

**Current Version**: 1.2.1  
**Python Compatibility**: 3.8+  
**License**: MIT  
**Repository**: [GitHub](https://github.com/dkdndes/pybiorythm)