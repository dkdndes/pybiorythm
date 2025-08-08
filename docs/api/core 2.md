# Core Functions API Reference

This document provides detailed API reference for the core functions and utilities in the PyBiorythm library.

## Module Overview

The `biorythm.core` module contains the fundamental building blocks for biorhythm calculations, date validation, user interface components, and utility functions.

```python
from biorythm.core import (
    BiorhythmCalculator,
    DateValidator,
    UserInterface,
    setup_logging,
    get_terminal_width,
    main
)
```

## Core Functions

### main()

The main entry point function that orchestrates the entire biorhythm calculation process.

```python
def main(
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    orientation: str = "vertical",
    days: Optional[int] = None,
) -> None
```

**Parameters:**

- `year` (int, optional): Birth year (1-9999). If None, enters interactive mode
- `month` (int, optional): Birth month (1-12). If None, enters interactive mode  
- `day` (int, optional): Birth day (1-31). If None, enters interactive mode
- `orientation` (str): Output format. Options: "vertical", "horizontal", "json-vertical", "json-horizontal". Default: "vertical"
- `days` (int, optional): Number of days to plot. If None, uses defaults based on orientation

**Raises:**

- `DateValidationError`: If date parameters are invalid
- `BiorhythmError`: If calculation fails
- `ChartParameterError`: If chart parameters are invalid

**Example:**
```python
from biorythm.core import main

# Interactive mode
main()

# Direct calculation
main(year=1990, month=5, day=15, orientation="vertical", days=30)

# JSON output
main(year=1990, month=5, day=15, orientation="json-vertical", days=7)
```

### setup_logging()

Configure logging system for the application.

```python
def setup_logging(level: int = logging.INFO) -> None
```

**Parameters:**

- `level` (int): Logging level from the `logging` module. Default: `logging.INFO`

**Example:**
```python
import logging
from biorythm.core import setup_logging

# Default INFO level logging
setup_logging()

# Debug level logging for development
setup_logging(logging.DEBUG)

# Error level logging for production
setup_logging(logging.ERROR)
```

### get_terminal_width()

Get the current terminal width with fallback handling.

```python
def get_terminal_width(default=80, min_width=40) -> int
```

**Parameters:**

- `default` (int): Default width if terminal width cannot be determined. Default: 80
- `min_width` (int): Minimum acceptable width. Default: 40

**Returns:**

- `int`: Terminal width in characters, at least `min_width`

**Example:**
```python
from biorythm.core import get_terminal_width

# Get current terminal width
width = get_terminal_width()

# Get width with custom defaults
width = get_terminal_width(default=120, min_width=60)

# Use for chart sizing
calc = BiorhythmCalculator(width=width)
```

## Utility Classes

### DateValidator

Static utility class for date validation and creation.

#### Methods

##### validate_date_components()

```python
@staticmethod
def validate_date_components(year: int, month: int, day: int) -> None
```

Validates individual date components before creating datetime objects.

**Parameters:**

- `year` (int): Year (1-9999)
- `month` (int): Month (1-12)
- `day` (int): Day (1-31)

**Raises:**

- `DateValidationError`: If any component is invalid

**Example:**
```python
from biorythm.core import DateValidator

# Valid date components
try:
    DateValidator.validate_date_components(1990, 5, 15)
    print("Date components are valid")
except DateValidationError as e:
    print(f"Invalid date: {e}")

# Invalid year
try:
    DateValidator.validate_date_components(10000, 5, 15)  # Year too large
except DateValidationError as e:
    print(f"Error: {e}")  # "Year must be between 1 and 9999"
```

##### create_validated_date()

```python
@staticmethod  
def create_validated_date(year: int, month: int, day: int) -> datetime
```

Creates a validated datetime object from components.

**Parameters:**

- `year` (int): Year (1-9999)
- `month` (int): Month (1-12)
- `day` (int): Day (1-31)

**Returns:**

- `datetime`: Validated datetime object

**Raises:**

- `DateValidationError`: If date is invalid or in the future

**Example:**
```python
from biorythm.core import DateValidator

# Create valid birthdate
birthdate = DateValidator.create_validated_date(1990, 5, 15)
print(birthdate)  # 1990-05-15 00:00:00

# Future date (will raise error)
try:
    future_date = DateValidator.create_validated_date(2030, 1, 1)
except DateValidationError as e:
    print(f"Error: {e}")  # "Birth date cannot be in the future"

# Invalid date (will raise error)
try:
    invalid_date = DateValidator.create_validated_date(2024, 2, 30)
except DateValidationError as e:
    print(f"Error: {e}")  # "Invalid date 2024-02-30"
```

### UserInterface

Interactive user interface for collecting input in terminal mode.

#### Methods

##### get_user_input()

```python
def get_user_input(self) -> Tuple[int, int, int, str, int]
```

Collect user input interactively with validation and educational information.

**Returns:**

- `tuple`: (year, month, day, orientation, days)

**Raises:**

- `DateValidationError`: If user provides invalid input

**Example:**
```python
from biorythm.core import UserInterface

ui = UserInterface()

try:
    year, month, day, orientation, days = ui.get_user_input()
    print(f"User selected: {year}-{month:02d}-{day:02d}")
    print(f"Orientation: {orientation}, Days: {days}")
except DateValidationError as e:
    print(f"Input error: {e}")
```

**Interactive Flow:**
```
Biorhythm Chart Generator (Pseudoscience Demonstration):
Historical Context:
• Developed by Wilhelm Fliess (friend of Sigmund Freud) in 1890s
• Popularized in USA during 1970s by Bernard Gittelson
• Extensively tested - no scientific evidence found
• All 134+ studies confirm it has no predictive value

  Enter your birth YEAR (1-9999): 1990
  Enter your birth MONTH (1-12): 5
  Enter your birth DAY (1-31): 15

Chart Orientation:
  1. Vertical (traditional, top-to-bottom timeline)
  2. Horizontal (left-to-right timeline)
  3. JSON (vertical data)
  4. JSON (horizontal data)
  Choose orientation (1,2,3,4) [default=1]: 1
  Enter number of days to plot [default=20]: 30
```

## Constants

The following constants are available for direct use:

### Cycle Constants
```python
PHYSICAL_CYCLE_DAYS = 23      # Physical biorhythm cycle length
EMOTIONAL_CYCLE_DAYS = 28     # Emotional biorhythm cycle length  
INTELLECTUAL_CYCLE_DAYS = 33  # Intellectual biorhythm cycle length
```

### Chart Constants
```python
MIN_CHART_WIDTH = 12          # Minimum allowed chart width
DEFAULT_CHART_WIDTH = 55      # Default chart width
DEFAULT_DAYS_TO_PLOT = 29     # Default number of days to plot
```

### Validation Constants
```python
MIN_YEAR = 1                  # Minimum allowed year
MAX_YEAR = 9999              # Maximum allowed year  
CRITICAL_DAY_THRESHOLD = 0.05 # Threshold for critical day detection
```

## Mathematical Functions

### Biorhythm Calculation

The core biorhythm calculation uses standard sine wave mathematics:

```python
# Core mathematical formula (implemented in BiorhythmCalculator)
days_alive = (target_date - birthdate).days

physical = math.sin((2 * math.pi * days_alive) / PHYSICAL_CYCLE_DAYS)
emotional = math.sin((2 * math.pi * days_alive) / EMOTIONAL_CYCLE_DAYS)  
intellectual = math.sin((2 * math.pi * days_alive) / INTELLECTUAL_CYCLE_DAYS)
```

**Mathematical Properties:**
- All cycle values range from -1.0 to +1.0
- Cycles are sinusoidal with different periods
- Critical days occur when cycle values approach zero (±0.05)
- Full cycle repetition occurs every 21,252 days (58.18 years)

### Cycle Interactions

**Cycle Repetition Patterns:**
```python
# Physical + Emotional cycles repeat every 644 days (1.76 years)
physical_emotional_repeat = 644

# All three cycles repeat every 21,252 days (58.18 years)
all_cycles_repeat = 21252

# Days until next repetition
days_to_pe_repeat = 644 - (days_alive % 644)
days_to_all_repeat = 21252 - (days_alive % 21252)
```

## Error Handling

### Exception Types

All exceptions inherit from `BiorhythmError`:

```python
# Base exception
class BiorhythmError(Exception):
    pass

# Date-related errors
class DateValidationError(BiorhythmError):
    pass

# Chart parameter errors  
class ChartParameterError(BiorhythmError):
    pass
```

### Common Error Scenarios

```python
from biorythm.core import DateValidator, BiorhythmCalculator

# Date validation errors
try:
    DateValidator.create_validated_date(2030, 1, 1)  # Future date
except DateValidationError as e:
    print(f"Date error: {e}")

try:
    DateValidator.create_validated_date(2024, 13, 1)  # Invalid month
except DateValidationError as e:
    print(f"Date error: {e}")

# Chart parameter errors
try:
    BiorhythmCalculator(width=5)  # Width too small
except ChartParameterError as e:
    print(f"Chart error: {e}")

try:
    BiorhythmCalculator(orientation="invalid")  # Invalid orientation
except ChartParameterError as e:
    print(f"Chart error: {e}")
```

## Performance Considerations

### Function Performance

- `main()`: O(days) - linear with number of days to calculate
- `DateValidator` methods: O(1) - constant time validation
- `get_terminal_width()`: O(1) - single system call
- `setup_logging()`: O(1) - one-time setup

### Memory Usage

- Minimal memory footprint
- No caching or large data structures
- Memory usage scales linearly with days calculated
- Safe for concurrent execution

## Integration Examples

### Basic Integration

```python
from biorythm.core import main, setup_logging
import logging

# Set up application logging
setup_logging(logging.INFO)

# Generate biorhythm chart
main(year=1990, month=5, day=15, orientation="vertical", days=30)
```

### Advanced Integration

```python
from biorythm.core import (
    BiorhythmCalculator, 
    DateValidator, 
    get_terminal_width,
    setup_logging
)
import logging
import json

# Configure logging
setup_logging(logging.DEBUG)

# Create validated birthdate
birthdate = DateValidator.create_validated_date(1990, 5, 15)

# Create calculator with terminal width
width = get_terminal_width()
calc = BiorhythmCalculator(width=width, days=90, orientation="horizontal")

# Generate different outputs
print("=== ASCII Chart ===")
calc.generate_chart(birthdate)

print("\n=== JSON Data ===")
json_data = calc.generate_timeseries_json(birthdate)
data = json.loads(json_data)
print(f"Generated {len(data['data'])} data points")
```

### Batch Processing

```python
from biorythm.core import BiorhythmCalculator, DateValidator
from datetime import datetime
import json

def process_multiple_birthdates(birthdates):
    """Process multiple birthdates and return combined results."""
    calc = BiorhythmCalculator(days=30)
    results = []
    
    for birth_year, birth_month, birth_day in birthdates:
        try:
            birthdate = DateValidator.create_validated_date(
                birth_year, birth_month, birth_day
            )
            json_data = calc.generate_timeseries_json(birthdate)
            data = json.loads(json_data)
            results.append(data)
        except Exception as e:
            print(f"Error processing {birth_year}-{birth_month}-{birth_day}: {e}")
    
    return results

# Process multiple people
birthdates = [
    (1990, 5, 15),
    (1985, 12, 3),
    (1995, 7, 22)
]

results = process_multiple_birthdates(birthdates)
print(f"Processed {len(results)} birthdates successfully")
```

---

**Next**: [JSON Schema](json-schema.md) | [Error Handling](errors.md) | [Calculator API](calculator.md)