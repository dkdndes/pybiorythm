# Biorhythm

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-72%20passed-green.svg)](https://github.com/dkdndes/pybiorythm)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)](https://github.com/dkdndes/pybiorythm)
[![CI/CD](https://github.com/dkdndes/pybiorythm/actions/workflows/ci.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/docker-multi--stage-blue.svg)](Dockerfile)
[![Security](https://github.com/dkdndes/pybiorythm/actions/workflows/codeql.yml/badge.svg)](https://github.com/dkdndes/pybiorythm/actions/workflows/codeql.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A Python library for generating biorhythm charts and timeseries data based on the pseudoscientific biorhythm theory.

## � Scientific Disclaimer

**This software implements biorhythm theory, which is considered PSEUDOSCIENCE.** Extensive scientific research has found NO VALIDITY to biorhythm theory beyond coincidence. Multiple controlled studies have consistently failed to find any correlation between the proposed 23, 28, and 33-day cycles and human performance or life events.

**This implementation is provided FOR ENTERTAINMENT PURPOSES ONLY** and should NOT be used for making any important life decisions.

## Installation

### Option 1: Docker (Recommended)

The easiest way to run the application with all dependencies:

```bash
# Pull and run (when published to Docker Hub)
docker run -it biorythm:latest

# Or build locally
git clone https://github.com/peterrosemann/biorythm.git
cd biorythm
docker build -t biorythm:latest .
docker run -it biorythm:latest
```

### Option 2: Python Package

```bash
# Install from PyPI (when published)
pip install biorythm

# Or install from source
git clone https://github.com/peterrosemann/biorythm.git
cd biorythm
pip install .
```

## Quick Start

### Command Line Usage

```bash
# Interactive mode
python main.py

# Command line with arguments
python main.py -y 1990 -m 5 -d 15

# Different chart orientations
python main.py -y 1990 -m 5 -d 15 --orientation horizontal
python main.py -y 1990 -m 5 -d 15 --orientation vertical --days 30

# Generate JSON output for data analysis
python main.py -y 1990 -m 5 -d 15 --orientation json-vertical
python main.py -y 1990 -m 5 -d 15 --orientation json-horizontal
```

### Programmatic Usage

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

## JSON Data Format for Developers

The `generate_timeseries_json()` method produces structured data perfect for:
- Time series analysis and visualization
- Testing data for analytics applications
- Machine learning training data
- Statistical analysis of periodic patterns

### Sample JSON Structure

```json
{
  "meta": {
    "generator": "biorhythm_enhanced.py",
    "version": "2025-08-07",
    "birthdate": "1990-05-15",
    "plot_date": "2025-08-07",
    "days_alive": 12837,
    "cycle_lengths_days": {
      "physical": 23,
      "emotional": 28,
      "intellectual": 33
    },
    "chart_orientation": "vertical",
    "days": 29,
    "width": 55,
    "scientific_warning": "�  SCIENTIFIC WARNING �\nBiorhythm theory is PSEUDOSCIENCE..."
  },
  "cycle_repeats": {
    "physical_emotional_repeat_in_days": 457,
    "all_cycles_repeat_in_days": 8415
  },
  "critical_days": [
    {
      "date": "2025-08-05",
      "cycles": "Physical cycle(s) near zero"
    }
  ],
  "data": [
    {
      "date": "2025-07-24",
      "days_alive": 12823,
      "physical": -0.8987940462991669,
      "emotional": 0.9744583088414919,
      "intellectual": -0.9510565162951536,
      "critical_cycles": []
    },
    ...
  ]
}
```

### Using JSON Data for Testing

The JSON output is ideal for:

**Time Series Analysis:**
```python
import json
import pandas as pd

# Load biorhythm data
with open('biorhythm_data.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data['data'])
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Analyze periodic patterns
print(df[['physical', 'emotional', 'intellectual']].describe())
```

**Mock Data Generation:**
```python
# Generate test data for different birthdates
from datetime import datetime, timedelta
from biorythm import BiorhythmCalculator

calc = BiorhythmCalculator(days=365)  # Full year
test_birthdates = [
    datetime(1980, 1, 1),
    datetime(1990, 6, 15),
    datetime(2000, 12, 31)
]

for birthdate in test_birthdates:
    data = calc.generate_timeseries_json(birthdate)
    # Use data for testing your analytics pipeline
```

## Historical Context

- **Developer**: Wilhelm Fliess (1858-1928), German otolaryngologist and friend of Sigmund Freud
- **Period**: Late 19th century (1890s)
- **Popularization**: United States in the 1970s by Bernard Gittelson
- **Scientific Status**: Thoroughly debunked by multiple peer-reviewed studies

## Cycle Information

- **Physical Cycle**: 23 days (coordination, strength, well-being)
- **Emotional Cycle**: 28 days (creativity, sensitivity, mood)  
- **Intellectual Cycle**: 33 days (alertness, analytical functioning)

**Pattern Repetition:**
- Physical + Emotional cycles repeat every 644 days (1.76 years)
- All three cycles repeat every 21,252 days (58.18 years)

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/peterrosemann/biorythm.git
cd biorythm

# Install development dependencies
pip install -e ".[dev]"

# Install additional testing dependencies
pip install pandas  # For JSON timeseries testing
```

### Running Tests

The project includes comprehensive test coverage (90%+) with pytest and automated coverage reporting:

```bash
# Run all tests with coverage (recommended)
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_biorhythm_calculator.py

# Run tests with detailed coverage report
pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser to view detailed coverage

# Run only fast tests (exclude slow integration tests)
pytest -m "not slow"

# Run only JSON-related tests
pytest -k "json"

# Fail if coverage drops below 85%
pytest --cov-fail-under=85
```

### Test Coverage Details

The project maintains high test coverage across all components:

| Component | Coverage | Description |
|-----------|----------|-------------|
| **Total Project** | **90%** | Overall test coverage across all modules |
| `biorythm.py` | 78% | Core biorhythm calculation and chart generation |
| `main.py` | 96% | Command line interface and argument parsing |
| All test files | 99%+ | Self-testing coverage verification |

**Coverage Infrastructure:**
- Automated coverage measurement with `pytest-cov`
- HTML reports for detailed line-by-line analysis
- Minimum coverage threshold enforcement (85%)
- Coverage exclusions for non-testable patterns (pragma: no cover, __main__, etc.)
- Integration with development workflow

### Test Structure

```
tests/
├── __init__.py                   # Test package initialization
├── conftest.py                   # Shared fixtures and configuration
├── test_biorhythm_calculator.py # Core functionality tests (31 tests)
├── test_biorythm_coverage.py    # Coverage-focused tests (9 tests)
├── test_main.py                  # Command line interface tests (18 tests)
└── test_json_timeseries.py      # JSON output and data analysis tests (14 tests)

Configuration:
├── pytest.ini                   # Pytest and coverage configuration
└── htmlcov/                     # Generated HTML coverage reports
```

### Test Categories

**Unit Tests** (`test_biorhythm_calculator.py`):
- BiorhythmCalculator class functionality
- Date validation and error handling
- Mathematical calculations accuracy
- Chart generation output validation

**Coverage Tests** (`test_biorythm_coverage.py`):
- Horizontal chart generation methods
- Different chart orientations (vertical/horizontal)
- JSON timeseries output functionality
- Edge cases and critical day detection
- Parameter validation and error handling

**CLI Tests** (`test_main.py`):
- Command line argument parsing
- Integration with main biorhythm module
- Error handling for invalid inputs
- Help and usage message validation

**JSON & Analytics Tests** (`test_json_timeseries.py`):
- JSON schema validation
- Data structure for timeseries analysis
- Pandas DataFrame integration
- Statistical properties validation
- Feature engineering capabilities
- Multi-subject analysis support

### Test Fixtures

Common test fixtures available in `conftest.py`:
- `sample_birthdate`: Standard birthdate for testing
- `basic_calculator`: Pre-configured calculator instance
- `json_calculator`: Calculator optimized for JSON testing
- `sample_json_data`: Pre-generated JSON data
- `multiple_birthdates`: Set of birthdates for comparative testing

### Testing Data Analysis Features

Special tests for developers using the JSON timeseries data:

```bash
# Test pandas integration
pytest tests/test_json_timeseries.py::TestTimeseriesDataAnalysis::test_pandas_integration

# Test statistical properties
pytest tests/test_json_timeseries.py::TestTimeseriesDataAnalysis::test_statistical_properties

# Test feature engineering capabilities  
pytest tests/test_json_timeseries.py::TestTimeseriesDataAnalysis::test_feature_engineering_potential
```

### Code Quality & Continuous Integration

**Quality Metrics:**
- ✅ **90% Test Coverage** with automated reporting
- ✅ **72 Passing Tests** across all components  
- ✅ **Ruff Code Formatting** and linting compliance
- ✅ **Type Hints** for better code documentation
- ✅ **Comprehensive Error Handling** with user-friendly messages

**Code Quality Tools:**

```bash
# Code formatting
ruff format .

# Linting and style checks
ruff check .

# Type checking (if mypy is installed)
mypy biorythm.py

# Run all quality checks with coverage
pytest --cov=. --cov-fail-under=85 && ruff check . && ruff format --check .
```

**Pre-commit Quality Gates:**
- All tests must pass (72/72)
- Coverage must be ≥ 85% (currently 90%)
- Code must pass ruff linting
- No unhandled type errors

## CI/CD & Automation

### GitHub Actions Workflows

The project includes comprehensive GitHub Actions for continuous integration and deployment:

**🔄 CI/CD Pipeline (`ci.yml`)**
- Multi-version Python testing (3.8-3.12)
- Code quality checks with Ruff
- Security scanning with Bandit and Safety  
- Docker build and testing
- Performance benchmarking
- Coverage reporting to Codecov

**🐳 Docker Publishing (`docker-publish.yml`)**
- Multi-architecture container builds (AMD64, ARM64)
- GitHub Container Registry publishing
- Vulnerability scanning with Trivy
- Security compliance validation

**🚀 Release Management (`release.yml`)**
- Automated GitHub releases
- PyPI package publishing
- Docker image tagging and distribution
- Release validation and testing

**🔒 Security Analysis (`codeql.yml`)**
- CodeQL static analysis
- Weekly automated security scans
- Vulnerability detection and reporting

**🔍 Dependency Review (`dependency-review.yml`)**
- Automated dependency vulnerability scanning
- License compliance checking
- PR-based dependency analysis

### Automation Features

- **📦 Dependabot:** Weekly automated dependency updates
- **🛡️ Security:** Continuous vulnerability monitoring
- **📋 Templates:** Standardized issue and PR templates  
- **✅ Quality Gates:** Automated quality enforcement
- **📊 Monitoring:** Performance and coverage tracking

See [`.github/WORKFLOWS.md`](.github/WORKFLOWS.md) for detailed workflow documentation.

### Running Performance Tests

```bash
# Test with large datasets (marked as slow)
pytest -m slow

# Test JSON serialization with large data
pytest tests/test_json_timeseries.py::TestJSONSerializationAndStorage::test_large_dataset_generation
```

## Docker Deployment

### Multi-Stage Production Docker Build

The project includes a highly optimized multi-stage Dockerfile:

**Stage 1 (Builder):** Development dependencies and build tools  
**Stage 2 (Production):** Minimal runtime with only numpy dependency

### Building Docker Images

```bash
# Build production image (recommended)
docker build --target production -t biorythm:latest .

# Or use the build script
./build-docker.sh

# Build development image (includes build tools)
docker build --target builder -t biorythm:dev .
```

### Running with Docker

```bash
# Interactive mode
docker run -it biorythm:latest

# With command line arguments
docker run biorythm:latest python main.py -y 1990 -m 5 -d 15

# Generate JSON output
docker run biorythm:latest python main.py -y 1990 -m 5 -d 15 --orientation json-vertical

# Using docker-compose
docker-compose up biorythm

# Development container (with volume mount)
docker-compose --profile dev up biorythm-dev
```

### Docker Image Details

**Production Image Features:**
- ✅ **Minimal size** - Python 3.12 slim base with only numpy
- ✅ **Security** - Non-root user execution  
- ✅ **Health checks** - Built-in application health monitoring
- ✅ **No test dependencies** - Tests, coverage, and dev tools excluded
- ✅ **Multi-architecture** - Compatible with AMD64 and ARM64

**Image Layers:**
```dockerfile
# Only essential components in production image:
python:3.12-slim           # Base runtime
numpy>=1.20.0             # Required dependency  
biorythm.py + main.py     # Application code
Non-root user setup       # Security hardening
```

**Excluded from Production Image:**
- All test files (`tests/`)
- Coverage reports (`htmlcov/`, `.coverage`)
- Development dependencies (`pytest`, `ruff`, etc.)
- Build tools (`gcc`, `g++`)
- Documentation files

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Educational Resources

- [Wikipedia: Biorhythm (pseudoscience)](https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience))
- [The Skeptic's Dictionary: Biorhythms](http://skepdic.com/biorhyth.html)
- "Comprehensive Review of Biorhythm Theory" by Terence Hines (1998)

---

**Remember**: This is pseudoscience with no proven validity! Use for entertainment and educational purposes only.