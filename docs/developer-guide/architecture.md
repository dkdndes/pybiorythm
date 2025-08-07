# Project Architecture

This document describes the overall architecture, design patterns, and structural decisions of the PyBiorythm project.

## Overview

PyBiorythm is designed as a modular, extensible Python library for biorhythm calculations with multiple output formats. The architecture emphasizes:

- **Separation of concerns** between calculation, visualization, and I/O
- **Testability** with dependency injection and clear interfaces
- **Extensibility** for new output formats and visualization types
- **Scientific integrity** with prominent pseudoscience disclaimers

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PyBiorythm System                        │
├─────────────────────────────────────────────────────────────┤
│  CLI Interface (main.py)                                    │
│  ├─ Command-line argument parsing                           │
│  ├─ Interactive user input                                  │
│  └─ Output format selection                                 │
├─────────────────────────────────────────────────────────────┤
│  Core Library (biorythm/core.py)                           │
│  ├─ BiorhythmCalculator: Main calculation engine            │
│  ├─ DateValidator: Input validation and sanitization        │
│  ├─ UserInterface: Interactive input handling               │
│  └─ Exception Classes: Structured error handling           │
├─────────────────────────────────────────────────────────────┤
│  Output Modules                                             │
│  ├─ ASCII Chart Generation (vertical/horizontal)            │
│  ├─ JSON Export (timeseries data)                          │
│  └─ Statistical Analysis (critical days, cycle info)       │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure                                             │
│  ├─ Logging and monitoring                                  │
│  ├─ Configuration management                                │
│  └─ Error handling and recovery                             │
└─────────────────────────────────────────────────────────────┘
```

## Module Structure

### Core Components

#### 1. BiorhythmCalculator

**Responsibility**: Core mathematical calculations and chart generation

```python
class BiorhythmCalculator:
    """
    Main calculator class handling:
    - Biorhythm mathematical computations
    - Chart visualization (ASCII art)
    - JSON data export
    - Critical day detection
    """
    
    def __init__(self, width: int, days: int, orientation: str):
        # Configuration and validation
    
    def calculate_biorhythm_values(self, birthdate, target_date):
        # Pure mathematical calculation
        
    def generate_chart(self, birthdate, plot_date):
        # Chart visualization orchestration
        
    def generate_timeseries_json(self, birthdate, plot_date):
        # Structured data export
```

**Design Patterns**:
- **Strategy Pattern**: Different chart orientations (vertical/horizontal)
- **Template Method**: Common chart generation workflow
- **Builder Pattern**: Flexible chart configuration

#### 2. DateValidator

**Responsibility**: Input validation and date handling

```python
class DateValidator:
    """
    Static utility class for:
    - Date component validation  
    - Safe datetime object creation
    - Future date prevention
    - Leap year handling
    """
    
    @staticmethod
    def validate_date_components(year, month, day):
        # Individual component validation
        
    @staticmethod  
    def create_validated_date(year, month, day):
        # Safe datetime creation with comprehensive checks
```

**Design Patterns**:
- **Static Factory**: Centralized date creation
- **Validator Pattern**: Input sanitization

#### 3. UserInterface

**Responsibility**: Interactive command-line interface

```python
class UserInterface:
    """
    Handles user interaction:
    - Input prompting and collection
    - Input validation and conversion
    - Educational information display
    - Error message presentation
    """
    
    def get_user_input(self):
        # Interactive input collection with validation
```

**Design Patterns**:
- **Facade Pattern**: Simplified interface for complex input handling
- **Command Pattern**: User action encapsulation

### Data Flow Architecture

```
Input Layer          Processing Layer         Output Layer
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ CLI Args    │────▶│ DateValidator    │────▶│ ASCII Charts    │
│ User Input  │     │ BiorhythmCalc    │     │ JSON Export     │
│ Config      │     │ Critical Day Det │     │ Statistics      │
└─────────────┘     └──────────────────┘     └─────────────────┘
       │                       │                       │
       └───────── Error Handling & Logging ───────────┘
```

## Design Patterns

### 1. Strategy Pattern - Chart Orientations

Different chart rendering strategies are encapsulated:

```python
class BiorhythmCalculator:
    def generate_chart(self, birthdate, plot_date):
        if self.orientation == "horizontal":
            self._create_combined_horizontal_wave_matrix(birthdate, plot_date)
        else:
            self._generate_vertical_chart(birthdate, plot_date)
```

**Benefits**:
- Easy to add new visualization types
- Clean separation between calculation and presentation
- Testable strategies in isolation

### 2. Template Method - Chart Generation

Common workflow with customizable steps:

```python
def generate_chart(self, birthdate, plot_date):
    # Template method defining the algorithm
    try:
        self._print_chart_header(birthdate, plot_date, days_alive)
        if self.orientation == "horizontal":
            self._create_horizontal_chart(birthdate, plot_date)  # Variant step
        else:
            self._generate_vertical_chart(birthdate, plot_date)  # Variant step
        self._print_scientific_disclaimer()  # Common step
    except Exception as e:
        self._handle_generation_error(e)  # Common error handling
```

### 3. Factory Pattern - Date Creation

Centralized, validated object creation:

```python
class DateValidator:
    @staticmethod
    def create_validated_date(year, month, day):
        # Factory method with validation
        DateValidator.validate_date_components(year, month, day)
        try:
            return datetime(year, month, day)
        except ValueError as e:
            raise DateValidationError(f"Invalid date: {e}")
```

### 4. Exception Hierarchy

Structured error handling with custom exceptions:

```python
class BiorhythmError(Exception):
    """Base exception for biorhythm operations"""
    pass

class DateValidationError(BiorhythmError):
    """Raised when date validation fails"""
    pass
    
class ChartParameterError(BiorhythmError):
    """Raised when chart parameters are invalid"""
    pass
```

## Mathematical Architecture

### Biorhythm Calculation Engine

The core mathematical model is based on sine wave calculations:

```python
def calculate_biorhythm_values(self, birthdate, target_date):
    days_alive = (target_date - birthdate).days
    
    # Three independent sine waves with different periods
    physical = math.sin((2 * math.pi * days_alive) / 23)      # 23-day cycle
    emotional = math.sin((2 * math.pi * days_alive) / 28)     # 28-day cycle  
    intellectual = math.sin((2 * math.pi * days_alive) / 33)  # 33-day cycle
    
    return physical, emotional, intellectual
```

**Mathematical Properties**:
- **Domain**: All real numbers (days since birth)
- **Range**: [-1, 1] for each cycle
- **Periodicity**: Cycles repeat at their respective periods
- **Phase**: All cycles start at 0 on birth date

### Critical Day Algorithm

Critical days are detected when cycle values approach zero:

```python
def is_critical_day(self, physical, emotional, intellectual):
    threshold = 0.05  # 5% threshold around zero
    critical_cycles = []
    
    if abs(physical) <= threshold:
        critical_cycles.append("Physical")
    if abs(emotional) <= threshold:
        critical_cycles.append("Emotional")  
    if abs(intellectual) <= threshold:
        critical_cycles.append("Intellectual")
        
    return len(critical_cycles) > 0, critical_cycles
```

## Visualization Architecture

### ASCII Chart System

Two visualization strategies with shared positioning logic:

```python
# Shared positioning calculation
def _calculate_chart_positions(self, physical, emotional, intellectual):
    p_pos = math.floor(physical * (self.midwidth - 1)) + self.midwidth
    e_pos = math.floor(emotional * (self.midwidth - 1)) + self.midwidth
    i_pos = math.floor(intellectual * (self.midwidth - 1)) + self.midwidth
    return p_pos, e_pos, i_pos

# Strategy-specific rendering
def _create_chart_line(self, p_pos, e_pos, i_pos, is_plot_date, is_critical):
    # Build ASCII line with cycle markers
    # Handle overlapping positions
    # Apply special formatting for critical days
```

### Chart Coordinate System

```
Vertical Chart (time flows down):
Date    PASSIVE  CRITICAL  ACTIVE
Aug 01  -------- : --------
Aug 02      p    :    e i
Aug 03      *    :        # p and e overlap
Aug 04           :   *    # All cycles overlap at center

Horizontal Chart (time flows right):
Physical  : -----p-----e-----i-----
Emotional : --e----*----i---------  # * = overlap
Intel     : ----i----e----p-------
Timeline  : Aug01 Aug02 Aug03 Aug04
```

## Data Architecture

### JSON Schema Structure

Structured data export follows a hierarchical schema:

```python
{
    "meta": {
        # Generation metadata
        "generator", "version", "birthdate", "plot_date",
        "days_alive", "cycle_lengths_days", "chart_orientation",
        "days", "width", "scientific_warning"
    },
    "cycle_repeats": {
        # Mathematical cycle information
        "physical_emotional_repeat_in_days",
        "all_cycles_repeat_in_days"
    },
    "critical_days": [
        # Array of critical day objects
        {"date": "YYYY-MM-DD", "cycles": "description"}
    ],
    "data": [
        # Daily timeseries array
        {
            "date": "YYYY-MM-DD",
            "days_alive": int,
            "physical": float,      # [-1, 1]
            "emotional": float,     # [-1, 1] 
            "intellectual": float,  # [-1, 1]
            "critical_cycles": []   # Array of critical cycle names
        }
    ]
}
```

## Configuration Architecture

### Constants and Configuration

Centralized configuration through module constants:

```python
# Mathematical constants
PHYSICAL_CYCLE_DAYS = 23
EMOTIONAL_CYCLE_DAYS = 28
INTELLECTUAL_CYCLE_DAYS = 33

# Display constants  
MIN_CHART_WIDTH = 12
DEFAULT_CHART_WIDTH = 55
DEFAULT_DAYS_TO_PLOT = 29

# Validation constants
MIN_YEAR = 1
MAX_YEAR = 9999
CRITICAL_DAY_THRESHOLD = 0.05
```

### Runtime Configuration

Calculator instances are configured at creation:

```python
calculator = BiorhythmCalculator(
    width=get_terminal_width(),  # Dynamic terminal detection
    days=user_specified_days,    # User preference
    orientation=selected_mode    # Runtime choice
)
```

## Error Handling Architecture

### Exception Hierarchy

Structured error handling with specific exception types:

```
Exception
└── BiorhythmError (base for all biorhythm errors)
    ├── DateValidationError (date input problems)
    └── ChartParameterError (configuration issues)
```

### Error Propagation Strategy

1. **Validation Layer**: Input validation with specific error messages
2. **Processing Layer**: Business logic errors with context
3. **Presentation Layer**: User-friendly error display

```python
try:
    birthdate = DateValidator.create_validated_date(year, month, day)
    calculator = BiorhythmCalculator(width, days, orientation)
    calculator.generate_chart(birthdate)
except DateValidationError as e:
    logger.error(f"Date validation failed: {e}")
    print(f"Error: {e}")
    sys.exit(1)
except BiorhythmError as e:
    logger.error(f"Calculation error: {e}")
    print(f"Error: {e}")
    sys.exit(1)
```

## Performance Architecture

### Computational Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Single calculation | O(1) | O(1) |
| Chart generation | O(n) where n=days | O(n) for output buffer |
| JSON export | O(n) | O(n) for data structure |
| Critical day detection | O(n) | O(k) where k=critical days |

### Memory Management

- **Streaming approach**: Charts generated line-by-line
- **Minimal buffering**: Only necessary data kept in memory
- **Garbage collection friendly**: No circular references

## Testing Architecture

### Test Structure Hierarchy

```
tests/
├── Unit Tests
│   ├── test_biorhythm_calculator.py  # Core calculation logic
│   ├── test_date_validation.py       # Input validation
│   └── test_chart_generation.py      # Output generation
├── Integration Tests  
│   ├── test_main.py                  # CLI interface
│   └── test_json_timeseries.py       # Data export
└── Performance Tests
    └── test_coverage_gaps.py         # Edge cases and benchmarks
```

### Test Patterns

- **Fixture-based setup**: Shared test data and configurations
- **Parameterized tests**: Multiple input scenarios
- **Mock objects**: External dependency isolation
- **Coverage enforcement**: 85% minimum coverage

## Security Architecture

### Input Validation

- **Date range validation**: Prevent extreme dates that could cause overflow
- **Parameter validation**: Ensure chart parameters are within reasonable bounds
- **Type checking**: Explicit type validation for all inputs

### Scientific Integrity

- **Prominent disclaimers**: Pseudoscience warnings in all outputs
- **Educational content**: Links to scientific resources
- **Clear limitations**: Explicit statement of entertainment-only purpose

## Deployment Architecture

### Package Structure

```
biorythm/
├── __init__.py          # Package initialization
├── core.py             # Main functionality
└── main.py             # CLI entry point

docs/                   # Documentation
├── api/               # API reference  
├── user-guide/        # User documentation
└── developer-guide/   # Development docs

tests/                 # Test suite
├── conftest.py        # Test configuration
└── test_*.py          # Test modules
```

### Build System

- **Modern Python packaging**: Uses `pyproject.toml` with hatchling
- **Semantic versioning**: Automated version management
- **Multi-format distribution**: Source and wheel distributions
- **Cross-platform support**: Windows, macOS, Linux

## Extension Points

### Adding New Output Formats

```python
class BiorhythmCalculator:
    def generate_output(self, format_type, birthdate, plot_date):
        """Factory method for different output formats"""
        if format_type == "ascii":
            return self.generate_chart(birthdate, plot_date)
        elif format_type == "json":
            return self.generate_timeseries_json(birthdate, plot_date)
        elif format_type == "csv":  # New format
            return self._generate_csv_export(birthdate, plot_date)
        else:
            raise ChartParameterError(f"Unknown format: {format_type}")
```

### Adding New Chart Types

```python
def generate_chart(self, birthdate, plot_date):
    chart_strategies = {
        "vertical": self._generate_vertical_chart,
        "horizontal": self._create_combined_horizontal_wave_matrix,
        "circular": self._generate_circular_chart,  # New strategy
        "3d": self._generate_3d_chart,             # New strategy
    }
    
    strategy = chart_strategies.get(self.orientation)
    if strategy:
        strategy(birthdate, plot_date)
    else:
        raise ChartParameterError(f"Unknown orientation: {self.orientation}")
```

## Future Architecture Considerations

### Scalability Enhancements

1. **Plugin system**: External chart renderers
2. **Caching layer**: Pre-computed cycle values
3. **Batch processing**: Multiple person calculations
4. **API framework**: REST/GraphQL interface

### Performance Optimizations

1. **Vectorized calculations**: NumPy integration for large datasets
2. **Parallel processing**: Multi-core chart generation
3. **Memory pooling**: Reuse of calculation buffers
4. **JIT compilation**: Numba acceleration for hot paths

### Integration Capabilities

1. **Database support**: Store historical calculations
2. **Web framework integration**: Flask/Django plugins
3. **Visualization libraries**: Matplotlib/Plotly backends
4. **Export formats**: PDF, SVG, PNG generation

## Design Principles

### 1. Single Responsibility Principle
Each class has one clear purpose:
- `BiorhythmCalculator`: Mathematical calculations and visualization
- `DateValidator`: Input validation and sanitization
- `UserInterface`: User interaction handling

### 2. Open/Closed Principle
Extension without modification:
- New chart orientations via strategy pattern
- New output formats via factory pattern
- New validation rules via validator composition

### 3. Dependency Inversion Principle
High-level modules don't depend on low-level modules:
- Calculator doesn't depend on specific UI implementation
- Chart generation doesn't depend on specific output format
- Validation doesn't depend on specific input source

### 4. Interface Segregation Principle
Clients depend only on interfaces they use:
- CLI interface separated from programmatic interface
- Chart generation separated from data export
- Validation separated from calculation

## Quality Attributes

### Maintainability
- **Modular design**: Clear separation of concerns
- **Comprehensive documentation**: Code and API documentation
- **Consistent coding standards**: Enforced via linting
- **Version control**: Git with semantic versioning

### Testability
- **Unit test coverage**: 85% minimum requirement
- **Integration testing**: End-to-end workflow validation
- **Performance testing**: Benchmark regression prevention
- **Automated testing**: CI/CD pipeline integration

### Usability
- **Clear error messages**: Specific, actionable feedback
- **Interactive interface**: Guided user input
- **Multiple output formats**: ASCII, JSON, statistics
- **Educational content**: Scientific context and disclaimers

### Reliability
- **Input validation**: Comprehensive parameter checking
- **Error handling**: Graceful failure with recovery options  
- **Logging**: Detailed operation tracking
- **Exception safety**: No partial state corruption

## See Also

- [Development Setup](setup.md) - Development environment configuration
- [Testing Guide](testing.md) - Testing strategy and implementation
- [API Reference](../api/) - Detailed API documentation
- [Contributing Guidelines](contributing.md) - Contribution process and standards