# Installation Guide

PyBiorythm supports multiple installation methods to suit different use cases and environments.

## Requirements

- **Python**: 3.8 or higher
- **Dependencies**: NumPy (automatically installed)
- **Optional**: pandas (for JSON data analysis)

## Installation Methods

### Option 1: uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package manager that handles virtual environments automatically:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install biorythm
uv add biorythm

# Or from source repository
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm
uv pip install -e .
```

### Option 2: pip (Traditional)

Standard pip installation:

```bash
# Install from PyPI (when published)
pip install biorythm

# Or install from source
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm
pip install .

# Development installation (editable)
pip install -e .
```

### Option 3: Docker (Easiest)

Docker provides the most reliable and portable installation:

```bash
# Pull and run the official image
docker run -it biorythm:latest

# Or build locally from source
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm
docker build -t biorythm:latest .
docker run -it biorythm:latest
```

#### Docker Options

**Production Image:**
```bash
# Minimal production image (~50MB)
docker build --target production -t biorythm:prod .
docker run biorythm:prod python main.py -y 1990 -m 5 -d 15
```

**Development Image:**
```bash
# Full development image with tools (~200MB)
docker build --target builder -t biorythm:dev .
docker run -v $(pwd):/app biorythm:dev pytest
```

### Option 4: Development Installation

For contributors and developers:

```bash
# Clone repository
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm

# Install with development dependencies (uv method)
uv sync --group dev

# Or install with documentation dependencies too
uv sync --group dev --group docs

# Or with pip
pip install -e ".[dev]"

# Verify installation
pytest
```

## Verification

Test your installation:

=== "Command Line"
    ```bash
    # Test basic functionality
    python main.py -y 1990 -m 5 -d 15
    
    # Should display a biorhythm chart
    ```

=== "Python Code"
    ```python
    from datetime import datetime
    from biorythm import BiorhythmCalculator
    
    calc = BiorhythmCalculator()
    calc.generate_chart(datetime(1990, 5, 15))
    
    # Should print a biorhythm chart
    ```

=== "Docker"
    ```bash
    docker run biorythm:latest python main.py -y 1990 -m 5 -d 15
    
    # Should display a biorhythm chart
    ```

## Dependencies

### Required Dependencies

- **numpy**: Mathematical calculations (automatically installed)

### Development Dependencies

Only needed for development and testing:

```bash
# Core development tools
pytest>=8.3.5          # Testing framework
pytest-cov>=5.0.0      # Coverage reporting
pytest-benchmark>=4.0.0 # Performance testing
ruff>=0.1.0            # Code linting and formatting

# Security and quality
bandit>=1.7.10         # Security analysis
safety>=3.6.0          # Vulnerability scanning

# Build and release
build>=1.2.2.post1     # Package building
twine>=6.1.0           # PyPI publishing
python-semantic-release>=8.0.0 # Version management

# SBOM and security compliance
cyclonedx-bom>=5.5.0   # Software Bill of Materials

# Documentation
mkdocs>=1.6.1          # Documentation site
mkdocs-material>=9.6.16 # Material theme
mkdocs-mermaid2-plugin>=1.2.1 # Diagram support

# Optional analysis tools
pandas>=2.0.3          # Data analysis (optional)
```

## Platform Support

### Supported Platforms

- ✅ **Linux** (Ubuntu 20.04+, RHEL 8+, Alpine)
- ✅ **macOS** (10.15+, including M1/M2 ARM64)
- ✅ **Windows** (10+, WSL recommended)
- ✅ **Docker** (Multi-architecture: AMD64, ARM64)

### Python Versions

- ✅ **Python 3.8** - Minimum supported version
- ✅ **Python 3.9** - Full support
- ✅ **Python 3.10** - Full support  
- ✅ **Python 3.11** - Full support
- ✅ **Python 3.12** - Recommended version (latest)

## Docker Image Details

### Production Image Features

- **Base**: Python 3.12 slim (Debian-based)
- **Size**: ~50MB compressed
- **Security**: Non-root user execution
- **Health**: Built-in health checks
- **Multi-arch**: AMD64 and ARM64 support

### Image Variants

```bash
# Latest stable release
docker pull biorythm:latest

# Specific version
docker pull biorythm:1.2.1

# Development version
docker pull biorythm:dev

# Multi-architecture (auto-selected)
docker pull biorythm:latest
```

## Troubleshooting

### Common Issues

#### Import Error: numpy

```bash
# Error: ModuleNotFoundError: No module named 'numpy'
# Solution: Ensure numpy is installed
pip install numpy>=1.20.0
```

#### Permission Denied (Docker)

```bash
# Error: Permission denied when running Docker
# Solution: Add user to docker group or use sudo
sudo docker run biorythm:latest
# Or add to docker group:
sudo usermod -aG docker $USER
```

#### Python Version Issues

```bash
# Error: Python version not supported
# Solution: Check Python version
python --version
# Upgrade if needed:
# Ubuntu: sudo apt install python3.12
# macOS: brew install python@3.12
# Windows: Download from python.org
```

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/dkdndes/pybiorythm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dkdndes/pybiorythm/discussions)
- **Documentation**: This site or [README.md](https://github.com/dkdndes/pybiorythm)

## Next Steps

After installation:

- **New Users**: [Quick Start Guide](quick-start.md)
- **Developers**: [Development Setup](../developer-guide/setup.md)
- **Docker Users**: [Docker Deployment](../deployment/docker.md)
- **CLI Usage**: [Command Line Interface](cli.md)