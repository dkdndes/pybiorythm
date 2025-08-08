# Testing Guide

PyBiorythm maintains comprehensive test coverage with automated testing, performance benchmarks, and quality assurance.

## Test Coverage Overview

### Current Metrics

| Component | Coverage | Tests | Description |
|-----------|----------|-------|-------------|
| **Overall Project** | **90%+** | 72 tests | Total coverage across all modules |
| `biorythm/core.py` | 78% | 31 tests | Core biorhythm calculations |
| `main.py` | 96% | 18 tests | Command line interface |
| Test files | 99%+ | Self-testing | Coverage validation |

### Coverage Reporting

**Live Coverage Dashboard:** [codecov.io/gh/dkdndes/pybiorythm](https://codecov.io/gh/dkdndes/pybiorythm)

**Coverage Integration:**
- ✅ **Automated Upload**: Every CI run uploads to Codecov
- ✅ **PR Comments**: Coverage diff on pull requests
- ✅ **Branch Comparison**: Coverage changes over time
- ✅ **File-Level**: Line-by-line coverage analysis
- ✅ **Trend Analysis**: Historical coverage tracking

**Local Coverage Reports:**
```bash
# Generate HTML coverage report
uv run pytest --cov=. --cov-report=html

# View detailed report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Test Structure

### Test Organization

```
tests/
├── __init__.py                   # Test package initialization
├── conftest.py                   # Shared fixtures and configuration
├── test_biorhythm_calculator.py # Core functionality tests (31 tests)
├── test_main.py                  # CLI interface tests (18 tests)
├── test_json_timeseries.py       # JSON output tests (14 tests)
└── test_coverage_gaps.py         # Edge case coverage (9 tests)
```

### Test Categories

#### 1. Unit Tests (`test_biorhythm_calculator.py`)
**Focus**: BiorhythmCalculator class functionality

```python
class TestBiorhythmCalculator:
    def test_initialization(self):
        """Test calculator initialization with various parameters"""
        
    def test_cycle_calculations(self):
        """Test biorhythm cycle mathematical accuracy"""
        
    def test_date_validation(self):
        """Test date validation and error handling"""
        
    def test_chart_generation(self):
        """Test ASCII chart output formatting"""
```

**Coverage Areas:**
- Mathematical calculations accuracy
- Date validation and error handling
- Chart generation and formatting
- Parameter validation

#### 2. CLI Tests (`test_main.py`)
**Focus**: Command line interface integration

```python
class TestMainFunction:
    def test_interactive_mode(self):
        """Test interactive user input handling"""
        
    def test_command_line_args(self):
        """Test argument parsing and validation"""
        
    def test_error_handling(self):
        """Test CLI error messages and exit codes"""
        
    def test_output_formats(self):
        """Test different output format generation"""
```

**Coverage Areas:**
- Argument parsing and validation
- Interactive mode user flow
- Error handling and messages
- Integration with core calculator

#### 3. JSON & Analytics Tests (`test_json_timeseries.py`)
**Focus**: Data analysis and JSON output

```python
class TestJSONOutput:
    def test_json_schema_validation(self):
        """Test JSON output structure and schema"""
        
    def test_pandas_integration(self):
        """Test DataFrame conversion and analysis"""
        
    def test_statistical_properties(self):
        """Test mathematical properties of data"""
        
    def test_large_dataset_generation(self):
        """Test performance with large datasets"""
```

**Coverage Areas:**
- JSON schema validation
- Data structure integrity
- pandas DataFrame integration
- Statistical properties validation
- Performance characteristics

#### 4. Coverage Tests (`test_coverage_gaps.py`)
**Focus**: Edge cases and completeness

```python
class TestCoverageGaps:
    def test_horizontal_charts(self):
        """Test horizontal chart generation methods"""
        
    def test_critical_day_detection(self):
        """Test critical day identification logic"""
        
    def test_edge_cases(self):
        """Test boundary conditions and edge cases"""
        
    def test_error_conditions(self):
        """Test error handling completeness"""
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=term-missing

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_biorhythm_calculator.py

# Run specific test class
uv run pytest tests/test_main.py::TestMainFunction

# Run specific test method
uv run pytest tests/test_json_timeseries.py::TestJSONOutput::test_schema_validation
```

### Test Selection

```bash
# Run tests matching pattern
uv run pytest -k "json" -v

# Run only fast tests (exclude slow benchmarks)
uv run pytest -m "not slow"

# Run only slow/benchmark tests
uv run pytest -m "slow"

# Run tests that failed last time
uv run pytest --lf

# Run until first failure
uv run pytest -x
```

### Coverage Analysis

```bash
# Generate terminal coverage report
uv run pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report
uv run pytest --cov=. --cov-report=html

# Generate XML coverage report (for CI)
uv run pytest --cov=. --cov-report=xml

# Fail if coverage drops below threshold
uv run pytest --cov-fail-under=85

# Show missing lines for specific module
uv run pytest --cov=biorythm --cov-report=term-missing
```

## Test Fixtures

### Shared Fixtures (`conftest.py`)

```python
@pytest.fixture
def sample_birthdate():
    """Standard birthdate for testing"""
    return datetime(1990, 5, 15)

@pytest.fixture
def basic_calculator():
    """Pre-configured calculator instance"""
    return BiorhythmCalculator(width=55, days=29)

@pytest.fixture
def json_calculator():
    """Calculator optimized for JSON testing"""
    return BiorhythmCalculator(days=7, orientation="vertical")

@pytest.fixture
def sample_json_data(json_calculator, sample_birthdate):
    """Pre-generated JSON data for testing"""
    return json_calculator.generate_timeseries_json(sample_birthdate)

@pytest.fixture
def multiple_birthdates():
    """Set of birthdates for comparative testing"""
    return [
        datetime(1980, 1, 1),
        datetime(1990, 6, 15),
        datetime(2000, 12, 31)
    ]
```

## Writing Tests

### Test Development Guidelines

#### 1. Test Structure
```python
class TestNewFeature:
    def test_basic_functionality(self):
        """Test the primary use case"""
        # Arrange
        calc = BiorhythmCalculator()
        birthdate = datetime(1990, 5, 15)
        
        # Act
        result = calc.some_method(birthdate)
        
        # Assert
        assert result is not None
        assert isinstance(result, expected_type)
    
    def test_edge_cases(self):
        """Test boundary conditions"""
        calc = BiorhythmCalculator()
        
        # Test edge cases
        with pytest.raises(ValueError):
            calc.some_method(invalid_input)
    
    @pytest.mark.parametrize("input,expected", [
        (datetime(1990, 5, 15), expected_output_1),
        (datetime(2000, 1, 1), expected_output_2),
    ])
    def test_multiple_inputs(self, input, expected):
        """Test with various inputs"""
        calc = BiorhythmCalculator()
        result = calc.some_method(input)
        assert result == expected
```

#### 2. Coverage-Focused Testing
```python
def test_all_code_paths(self):
    """Ensure all conditional branches are tested"""
    calc = BiorhythmCalculator()
    
    # Test positive path
    result_pos = calc.method(positive_input)
    assert result_pos.condition
    
    # Test negative path  
    result_neg = calc.method(negative_input)
    assert not result_neg.condition
    
    # Test edge conditions
    result_edge = calc.method(edge_input)
    assert result_edge.special_handling
```

#### 3. Performance Testing
```python
@pytest.mark.slow
@pytest.mark.benchmark
def test_performance_large_dataset(benchmark):
    """Test performance with large datasets"""
    calc = BiorhythmCalculator(days=365)
    birthdate = datetime(1990, 5, 15)
    
    # Benchmark the operation
    result = benchmark(calc.generate_timeseries_json, birthdate)
    
    # Verify performance expectations
    data = json.loads(result)
    assert len(data['data']) == 365
    assert benchmark.stats.mean < 0.1  # < 100ms
```

## Performance Testing

### Benchmark Tests

```bash
# Run performance benchmarks
uv run pytest -m benchmark --benchmark-only

# Generate benchmark report
uv run pytest -m benchmark --benchmark-html=benchmarks.html

# Compare benchmarks over time
uv run pytest -m benchmark --benchmark-compare
```

### Performance Targets

| Operation | Target Time | Dataset Size |
|-----------|-------------|--------------|
| **Chart Generation** | < 1ms | 29 days |
| **JSON Generation** | < 10ms | 365 days |
| **Calculations** | < 0.1ms | Single date |
| **Large Dataset** | < 100ms | 1000 days |

### Memory Usage Testing

```python
import psutil
import pytest

def test_memory_usage():
    """Test memory efficiency"""
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    
    # Generate large dataset
    calc = BiorhythmCalculator(days=1000)
    result = calc.generate_timeseries_json(datetime(1990, 5, 15))
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Should not use more than 50MB for large datasets
    assert memory_increase < 50 * 1024 * 1024
```

## Data Analysis Testing

### pandas Integration Tests

```python
def test_pandas_integration(sample_json_data):
    """Test JSON to DataFrame conversion"""
    import pandas as pd
    
    data = json.loads(sample_json_data)
    df = pd.DataFrame(data['data'])
    df['date'] = pd.to_datetime(df['date'])
    
    # Validate DataFrame structure
    assert len(df.columns) == 5
    assert 'physical' in df.columns
    assert 'emotional' in df.columns
    assert 'intellectual' in df.columns
    
    # Validate data types
    assert df['physical'].dtype == float
    assert pd.api.types.is_datetime64_any_dtype(df['date'])
    
    # Validate value ranges
    assert df['physical'].between(-1, 1).all()
    assert df['emotional'].between(-1, 1).all()
    assert df['intellectual'].between(-1, 1).all()
```

### Statistical Property Tests

```python
def test_statistical_properties(sample_json_data):
    """Test mathematical properties of biorhythm data"""
    import pandas as pd
    import numpy as np
    
    data = json.loads(sample_json_data)
    df = pd.DataFrame(data['data'])
    
    # Test sine wave properties
    physical = df['physical'].values
    
    # Should have approximately zero mean over full cycles
    assert abs(np.mean(physical)) < 0.1
    
    # Should have standard deviation close to 1/√2 for sine wave
    expected_std = 1 / np.sqrt(2)
    assert abs(np.std(physical) - expected_std) < 0.1
    
    # Frequency analysis
    fft = np.fft.fft(physical)
    dominant_freq = np.argmax(np.abs(fft[1:len(fft)//2])) + 1
    
    # Should show 23-day cycle for physical rhythm
    cycle_length = len(physical) / dominant_freq
    assert abs(cycle_length - 23) < 2  # Allow some variance
```

## Continuous Integration Testing

### GitHub Actions Integration

**CI Test Pipeline:**
```yaml
# .github/workflows/ci.yml (excerpt)
- name: Run tests with coverage
  run: |
    uv run pytest --cov=. --cov-report=xml --cov-fail-under=85
    
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
    fail_ci_if_error: true
```

**Coverage Requirements:**
- **Minimum**: 85% overall coverage
- **Target**: 90%+ for new code
- **Enforcement**: CI fails if coverage drops

### Quality Gates

**Pre-merge Requirements:**
- ✅ All tests must pass (72/72)
- ✅ Coverage ≥ 85% maintained
- ✅ No security vulnerabilities
- ✅ Code formatting compliant
- ✅ No linting errors

## Test Data Management

### Mock Data Generation

```python
def generate_test_biorhythm_data(
    birthdate: datetime,
    days: int = 30,
    include_critical: bool = True
) -> dict:
    """Generate consistent test data"""
    calc = BiorhythmCalculator(days=days)
    return json.loads(calc.generate_timeseries_json(birthdate))

# Usage in tests
@pytest.fixture
def consistent_test_data():
    return generate_test_biorhythm_data(
        birthdate=datetime(1990, 5, 15),
        days=30
    )
```

### Test Data Validation

```python
def validate_json_schema(json_data: str) -> bool:
    """Validate JSON against expected schema"""
    import jsonschema
    
    schema = {
        "type": "object",
        "required": ["meta", "data"],
        "properties": {
            "meta": {
                "type": "object",
                "required": ["birthdate", "days_alive"]
            },
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["date", "physical", "emotional", "intellectual"]
                }
            }
        }
    }
    
    try:
        jsonschema.validate(json.loads(json_data), schema)
        return True
    except jsonschema.ValidationError:
        return False
```

## Debugging Tests

### Test Debugging Techniques

```bash
# Run single test with maximum verbosity
uv run pytest tests/test_specific.py::test_method -vvv

# Drop into debugger on failure
uv run pytest --pdb

# Drop into debugger on first failure
uv run pytest --pdb -x

# Show local variables in tracebacks
uv run pytest --tb=long

# Show full diff for assertion failures
uv run pytest -vv
```

### Test Logging

```python
import logging

def test_with_logging(caplog):
    """Test with log capture"""
    with caplog.at_level(logging.DEBUG):
        result = some_function_that_logs()
        
    # Check log messages
    assert "Expected log message" in caplog.text
    assert caplog.records[0].levelname == "DEBUG"
```

## Test Maintenance

### Keeping Tests Updated

**Regular Maintenance:**
- **Weekly**: Review test coverage reports
- **Per PR**: Ensure new code has tests
- **Monthly**: Update test dependencies
- **Per Release**: Validate end-to-end scenarios

**Test Quality Metrics:**
- Test execution time should remain under 30 seconds
- New features require 90%+ test coverage
- Flaky tests must be fixed or removed
- Test code should be documented

### Performance Monitoring

```bash
# Monitor test execution time
uv run pytest --durations=10

# Profile slow tests
uv run pytest --profile

# Generate test timing report
uv run pytest --benchmark-histogram
```

## Resources

### Testing Tools
- **pytest**: Primary testing framework
- **pytest-cov**: Coverage measurement
- **pytest-benchmark**: Performance testing
- **hypothesis**: Property-based testing (optional)

### Coverage Tools  
- **Codecov**: Online coverage dashboard
- **coverage.py**: Local coverage analysis
- **HTML Reports**: Interactive coverage browsing

### Links
- **Coverage Dashboard**: [codecov.io/gh/dkdndes/pybiorythm](https://codecov.io/gh/dkdndes/pybiorythm)
- **CI Logs**: GitHub Actions test execution
- **Test Reports**: Downloadable from CI artifacts

---

**Next Steps:**
- [Code Quality Standards](code-quality.md)
- [Development Setup](setup.md)
- [Contributing Guidelines](contributing.md)
- [CI/CD Pipeline](../workflows/github-actions.md)