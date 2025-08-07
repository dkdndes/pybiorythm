# Testing Guide

This guide covers the testing framework, practices, and standards for the PyBiorythm project.

## Overview

The project uses a comprehensive testing strategy with:
- **pytest** for test execution and fixtures
- **pytest-cov** for coverage reporting and enforcement  
- **pytest-benchmark** for performance regression testing
- **85% minimum code coverage** requirement
- Automated testing via GitHub Actions

## Test Structure

```
tests/
├── conftest.py                   # Shared fixtures and configuration
├── test_biorhythm_calculator.py  # Core functionality tests
├── test_main.py                  # CLI interface tests  
├── test_json_timeseries.py       # JSON output tests
└── test_coverage_gaps.py         # Edge case coverage
```

## Running Tests

### Local Testing

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=. --cov-report=term-missing

# Run with coverage requirement enforcement
uv run pytest --cov=. --cov-fail-under=85

# Generate HTML coverage report  
uv run pytest --cov=. --cov-report=html
# View in htmlcov/index.html
```

### Specific Test Execution

```bash
# Run specific test file
uv run pytest tests/test_biorhythm_calculator.py

# Run specific test class
uv run pytest tests/test_biorhythm_calculator.py::TestBiorhythmCalculator

# Run specific test method
uv run pytest tests/test_main.py::TestMainFunction::test_interactive_mode

# Run tests matching pattern
uv run pytest -k "json" -v

# Run only fast tests (exclude slow benchmarks)
uv run pytest -m "not slow"
```

### GitHub Actions Testing

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main`
- Python versions: 3.9, 3.10, 3.11, 3.12
- Multiple operating systems: Ubuntu, Windows, macOS

## Test Categories

### Unit Tests

Test individual functions and methods in isolation.

```python
import pytest
from datetime import datetime
from biorythm.core import BiorhythmCalculator, DateValidationError

class TestBiorhythmCalculator:
    def test_calculate_biorhythm_values(self):
        """Test biorhythm value calculations"""
        calc = BiorhythmCalculator()
        birthdate = datetime(1990, 5, 15)
        target_date = datetime(1990, 5, 15)  # Same day = all zeros
        
        physical, emotional, intellectual = calc.calculate_biorhythm_values(
            birthdate, target_date
        )
        
        # Values should be at zero on birth date
        assert abs(physical) < 0.01
        assert abs(emotional) < 0.01
        assert abs(intellectual) < 0.01

    def test_critical_day_detection(self):
        """Test critical day identification"""
        calc = BiorhythmCalculator()
        
        # Test critical day (values near zero)
        is_critical, cycles = calc.is_critical_day(0.02, -0.03, 0.5)
        assert is_critical is True
        assert "Physical" in cycles
        assert "Emotional" in cycles
        assert "Intellectual" not in cycles
```

### Integration Tests

Test component interactions and full workflows.

```python
class TestChartGeneration:
    def test_vertical_chart_generation(self, capsys):
        """Test complete vertical chart generation"""
        calc = BiorhythmCalculator(width=30, days=7, orientation="vertical")
        birthdate = datetime(1990, 5, 15)
        
        calc.generate_chart(birthdate)
        
        captured = capsys.readouterr()
        assert "BIORHYTHM CHART (VERTICAL)" in captured.out
        assert "Physical (23-day cycle)" in captured.out
        assert "CRITICAL DAYS" in captured.out or "No critical days" in captured.out

    def test_json_output_structure(self):
        """Test JSON output format and content"""
        calc = BiorhythmCalculator(days=5)
        birthdate = datetime(1990, 5, 15)
        
        data = calc.generate_timeseries_json(birthdate)
        
        # Validate structure
        assert "meta" in data
        assert "data" in data
        assert "critical_days" in data
        assert "cycle_repeats" in data
        
        # Validate metadata
        assert data["meta"]["birthdate"] == "1990-05-15"
        assert len(data["data"]) == 5
        
        # Validate data entries
        for entry in data["data"]:
            assert "date" in entry
            assert "physical" in entry
            assert -1.0 <= entry["physical"] <= 1.0
```

### Error Handling Tests

Test exception cases and error conditions.

```python
class TestErrorHandling:
    def test_invalid_date_validation(self):
        """Test date validation errors"""
        from biorythm.core import DateValidator
        
        with pytest.raises(DateValidationError):
            DateValidator.create_validated_date(2030, 5, 15)  # Future date
            
        with pytest.raises(DateValidationError):
            DateValidator.create_validated_date(1990, 13, 15)  # Invalid month
            
        with pytest.raises(DateValidationError):
            DateValidator.create_validated_date(1990, 2, 30)  # Invalid day

    def test_chart_parameter_validation(self):
        """Test chart parameter validation"""
        from biorythm.core import ChartParameterError
        
        with pytest.raises(ChartParameterError):
            BiorhythmCalculator(width=-1)  # Negative width
            
        with pytest.raises(ChartParameterError):
            BiorhythmCalculator(days=0)  # Zero days
            
        with pytest.raises(ChartParameterError):
            BiorhythmCalculator(orientation="invalid")  # Invalid orientation
```

### Performance Tests

Benchmark critical operations for regression testing.

```python
import pytest

class TestPerformance:
    @pytest.mark.benchmark
    def test_calculation_performance(self, benchmark):
        """Benchmark biorhythm calculation performance"""
        calc = BiorhythmCalculator()
        birthdate = datetime(1990, 5, 15)
        target_date = datetime.now()
        
        result = benchmark(calc.calculate_biorhythm_values, birthdate, target_date)
        
        # Ensure calculation is fast enough
        assert len(result) == 3  # Returns three values

    @pytest.mark.benchmark
    def test_chart_generation_performance(self, benchmark):
        """Benchmark chart generation performance"""
        calc = BiorhythmCalculator(days=30)
        birthdate = datetime(1990, 5, 15)
        
        # Should complete within reasonable time
        benchmark(calc.generate_chart, birthdate)

    @pytest.mark.slow
    def test_large_dataset_performance(self):
        """Test performance with large datasets"""
        calc = BiorhythmCalculator(days=365)  # Full year
        birthdate = datetime(1990, 5, 15)
        
        import time
        start_time = time.time()
        
        data = calc.generate_timeseries_json(birthdate)
        
        elapsed = time.time() - start_time
        
        # Should process year of data quickly
        assert elapsed < 5.0  # Less than 5 seconds
        assert len(data["data"]) == 365
```

## Test Configuration

### pytest.ini

```ini
[tool:pytest]
minversion = 6.0
addopts = 
    -ra
    --strict-markers
    --strict-config
    --cov=biorythm
    --cov-report=term-missing:skip-covered
    --cov-fail-under=85
testpaths = tests
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    benchmark: marks tests as performance benchmarks
```

### conftest.py

```python
import pytest
from datetime import datetime
from biorythm.core import BiorhythmCalculator

@pytest.fixture
def sample_birthdate():
    """Standard birthdate for testing"""
    return datetime(1990, 5, 15)

@pytest.fixture
def calculator():
    """Standard calculator instance"""
    return BiorhythmCalculator(width=30, days=7)

@pytest.fixture
def calculator_horizontal():
    """Horizontal orientation calculator"""
    return BiorhythmCalculator(width=30, days=7, orientation="horizontal")

@pytest.fixture
def mock_current_date():
    """Mock current date for consistent testing"""
    return datetime(2025, 8, 7)

# Configure markers
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "benchmark: mark test as performance benchmark")
```

## Coverage Requirements

### Minimum Coverage: 85%

All code must maintain at least 85% test coverage:

```bash
# Check current coverage
uv run pytest --cov=. --cov-report=term-missing --cov-fail-under=85

# View detailed coverage report
uv run pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Coverage Exclusions

Some code is excluded from coverage requirements:

```python
# pyproject.toml
[tool.coverage.run]
omit = [
    "_version.py",
    "*/tests/*",
    "*/venv/*",
    "*/.venv/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
]
```

## Test Data Management

### Sample Data

Use consistent test data for reproducible results:

```python
# Standard test cases
SAMPLE_BIRTHDATES = [
    datetime(1990, 5, 15),   # Standard case
    datetime(1980, 1, 1),    # New year birth
    datetime(2000, 2, 29),   # Leap year birth
    datetime(1995, 12, 31),  # Year-end birth
]

SAMPLE_DATES = [
    datetime(2025, 8, 7),    # Current test date
    datetime(2025, 1, 1),    # Year start
    datetime(2025, 12, 31),  # Year end
]
```

### Fixtures for Complex Data

```python
@pytest.fixture
def biorhythm_timeseries_data():
    """Generate sample timeseries data"""
    calc = BiorhythmCalculator(days=14)
    birthdate = datetime(1990, 5, 15)
    return calc.generate_timeseries_json(birthdate)

@pytest.fixture
def critical_day_scenario():
    """Create scenario with known critical days"""
    # Calculate specific dates that will be critical
    calc = BiorhythmCalculator(days=60)
    birthdate = datetime(1990, 1, 1)
    data = calc.generate_timeseries_json(birthdate)
    
    # Return data with guaranteed critical days
    return [entry for entry in data["data"] if entry["critical_cycles"]]
```

## Continuous Integration

### GitHub Actions Configuration

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Install UV
      uses: astral-sh/setup-uv@v6
      
    - name: Install dependencies
      run: uv sync --group dev
      
    - name: Run tests with coverage
      run: uv run pytest --cov=. --cov-report=xml --cov-fail-under=85
      
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Best Practices

### Test Organization

1. **One concept per test**: Each test should verify one specific behavior
2. **Descriptive names**: Test names should clearly describe what they verify
3. **AAA pattern**: Arrange, Act, Assert structure
4. **Independent tests**: Tests should not depend on each other

### Example Test Structure

```python
class TestBiorhythmCalculation:
    """Tests for core biorhythm calculation functionality"""
    
    def test_physical_cycle_calculation_on_birth_date(self):
        """Physical cycle should be zero on birth date"""
        # Arrange
        calc = BiorhythmCalculator()
        birthdate = datetime(1990, 5, 15)
        
        # Act  
        physical, _, _ = calc.calculate_biorhythm_values(birthdate, birthdate)
        
        # Assert
        assert abs(physical) < 0.01, "Physical cycle should be near zero on birth date"

    def test_cycle_values_within_valid_range(self):
        """All cycle values should be between -1 and 1"""
        # Arrange
        calc = BiorhythmCalculator()
        birthdate = datetime(1990, 5, 15)
        test_date = datetime(2025, 8, 7)
        
        # Act
        physical, emotional, intellectual = calc.calculate_biorhythm_values(
            birthdate, test_date
        )
        
        # Assert
        assert -1 <= physical <= 1, f"Physical value {physical} out of range"
        assert -1 <= emotional <= 1, f"Emotional value {emotional} out of range"  
        assert -1 <= intellectual <= 1, f"Intellectual value {intellectual} out of range"
```

### Mock and Patch Usage

```python
from unittest.mock import patch, mock_open
import pytest

class TestFileOperations:
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_json_export(self, mock_json_dump, mock_file):
        """Test JSON file export functionality"""
        calc = BiorhythmCalculator()
        data = {"test": "data"}
        
        # Test the export (if such functionality existed)
        # calc.export_json(data, "test.json")
        
        mock_file.assert_called_once_with("test.json", "w")
        mock_json_dump.assert_called_once()

    @patch("datetime.datetime")
    def test_current_date_calculation(self, mock_datetime):
        """Test calculation using mocked current date"""
        # Mock datetime.now() to return specific date
        mock_datetime.now.return_value = datetime(2025, 8, 7, 12, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        calc = BiorhythmCalculator()
        # Test functionality that depends on current date
```

## Debugging Tests

### Verbose Output

```bash
# Run with maximum verbosity
uv run pytest -vvv

# Show local variables on failure
uv run pytest -l

# Drop into debugger on failure
uv run pytest --pdb

# Run specific test with debugging
uv run pytest tests/test_main.py::test_specific_function -vvv --pdb
```

### Logging in Tests

```python
import logging

def test_with_logging(caplog):
    """Test with log capture"""
    with caplog.at_level(logging.INFO):
        calc = BiorhythmCalculator()
        # ... test code ...
    
    # Check log messages
    assert "BiorhythmCalculator initialized" in caplog.text
    assert caplog.records[0].levelname == "INFO"
```

### Temporary Files

```python
import tempfile
import json

def test_json_file_operations(tmp_path):
    """Test operations with temporary files"""
    # Create temporary file
    test_file = tmp_path / "test_data.json"
    
    # Generate and save data
    calc = BiorhythmCalculator(days=5)
    data = calc.generate_timeseries_json(datetime(1990, 5, 15))
    
    with open(test_file, "w") as f:
        json.dump(data, f)
    
    # Verify file contents
    with open(test_file, "r") as f:
        loaded_data = json.load(f)
    
    assert loaded_data["meta"]["days"] == 5
```

## Performance Monitoring

### Benchmark Tracking

```bash
# Run benchmarks and save results
uv run pytest --benchmark-only --benchmark-json=benchmark.json

# Compare benchmark results
uv run pytest --benchmark-compare=previous_benchmark.json

# Set performance thresholds
uv run pytest --benchmark-max-time=2.0
```

### Memory Usage Testing

```python
import psutil
import os

def test_memory_usage():
    """Monitor memory usage during large operations"""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Perform memory-intensive operation
    calc = BiorhythmCalculator(days=1000)
    data = calc.generate_timeseries_json(datetime(1990, 5, 15))
    
    final_memory = process.memory_info().rss
    memory_increase = (final_memory - initial_memory) / 1024 / 1024  # MB
    
    # Assert memory usage is reasonable
    assert memory_increase < 50, f"Memory usage increased by {memory_increase:.1f}MB"
```

## Scientific Validity Testing

### Pseudoscience Disclaimers

```python
def test_scientific_warnings_present():
    """Ensure scientific disclaimers are present in outputs"""
    calc = BiorhythmCalculator()
    data = calc.generate_timeseries_json(datetime(1990, 5, 15))
    
    warning = data["meta"]["scientific_warning"]
    assert "PSEUDOSCIENCE" in warning
    assert "NO scientific evidence" in warning
    assert "ENTERTAINMENT PURPOSES ONLY" in warning
```

### Mathematical Accuracy

```python
import math

def test_cycle_mathematical_accuracy():
    """Verify mathematical correctness of cycle calculations"""
    calc = BiorhythmCalculator()
    birthdate = datetime(1990, 5, 15)
    
    # Test known mathematical properties
    # Physical cycle (23 days) should repeat after 23 days
    base_date = datetime(2025, 8, 7)
    cycle_date = base_date + timedelta(days=23)
    
    p1, _, _ = calc.calculate_biorhythm_values(birthdate, base_date)
    p2, _, _ = calc.calculate_biorhythm_values(birthdate, cycle_date)
    
    # Values should be very close (accounting for floating-point precision)
    assert abs(p1 - p2) < 0.001, "23-day physical cycle should repeat"

def test_cycle_amplitude_bounds():
    """Verify cycle values never exceed mathematical bounds"""
    calc = BiorhythmCalculator()
    birthdate = datetime(1970, 1, 1)  # Long time span
    
    # Test many dates to ensure bounds
    test_dates = [datetime(1970, 1, 1) + timedelta(days=i) for i in range(0, 10000, 100)]
    
    for test_date in test_dates:
        p, e, i = calc.calculate_biorhythm_values(birthdate, test_date)
        
        # Sine function bounds: -1 ≤ sin(x) ≤ 1
        assert -1 <= p <= 1, f"Physical {p} exceeds bounds on {test_date}"
        assert -1 <= e <= 1, f"Emotional {e} exceeds bounds on {test_date}"
        assert -1 <= i <= 1, f"Intellectual {i} exceeds bounds on {test_date}"
```

## Test Maintenance

### Regular Test Review

- Review test coverage monthly
- Update tests when adding new features
- Remove obsolete tests for removed functionality
- Refactor tests to match code improvements

### Documentation Updates

- Keep test documentation current with code changes
- Update examples when API changes
- Document new test patterns and practices
- Maintain test data consistency

## Troubleshooting

### Common Test Failures

1. **Coverage failures**: Check uncovered lines with `--cov-report=term-missing`
2. **Date-sensitive tests**: Use fixed dates or mocking
3. **Platform differences**: Test on multiple OS if needed
4. **Performance variations**: Use reasonable thresholds in benchmarks

### Test Environment Issues

```bash
# Clean test environment
uv sync --group dev  # Reinstall dependencies
rm -rf .pytest_cache  # Clear pytest cache
rm -rf htmlcov/  # Remove old coverage reports

# Reset UV environment
uv clean  # Clear UV cache
rm -rf .venv  # Remove virtual environment
uv sync --group dev  # Recreate environment
```

## See Also

- [Development Setup](setup.md) - Setting up development environment
- [Code Quality](../workflows/code-quality.md) - Code quality standards
- [Architecture](architecture.md) - Project architecture overview
- [Contributing](contributing.md) - Contribution guidelines