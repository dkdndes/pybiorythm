# Core API Reference

The `biorythm.core` module contains the core functionality for biorhythm calculations and chart generation.

## Classes

### BiorhythmCalculator

Main class for calculating and visualizing biorhythm charts.

```python
from biorythm.core import BiorhythmCalculator
from datetime import datetime

calculator = BiorhythmCalculator(
    width=55,           # Chart width (default: 55)
    days=29,           # Number of days to plot (default: 29)
    orientation="vertical"  # Chart orientation: "vertical" or "horizontal"
)
```

#### Methods

##### `calculate_biorhythm_values(birthdate: datetime, target_date: datetime) -> Tuple[float, float, float]`

Calculate biorhythm values for a specific date.

**Parameters:**
- `birthdate`: Date of birth
- `target_date`: Date to calculate biorhythm for

**Returns:**
- Tuple of (physical, emotional, intellectual) values between -1.0 and 1.0

**Example:**
```python
from datetime import datetime

calculator = BiorhythmCalculator()
birthdate = datetime(1990, 5, 15)
target_date = datetime.now()

physical, emotional, intellectual = calculator.calculate_biorhythm_values(
    birthdate, target_date
)

print(f"Physical: {physical:.2f}")
print(f"Emotional: {emotional:.2f}")
print(f"Intellectual: {intellectual:.2f}")
```

##### `generate_chart(birthdate: datetime, plot_date: datetime = None) -> None`

Generate and display a biorhythm chart.

**Parameters:**
- `birthdate`: Date of birth
- `plot_date`: Date to center the chart on (default: today)

**Example:**
```python
calculator = BiorhythmCalculator(orientation="horizontal")
birthdate = datetime(1990, 5, 15)
calculator.generate_chart(birthdate)
```

##### `generate_timeseries_json(birthdate: datetime, plot_date: datetime = None, chart_orientation: str = "vertical") -> dict`

Generate biorhythm data as JSON for analytics or API usage.

**Parameters:**
- `birthdate`: Date of birth
- `plot_date`: Center date for the timeseries (default: today)
- `chart_orientation`: Orientation metadata ("vertical" or "horizontal")

**Returns:**
- Dictionary containing metadata, timeseries data, and critical days

**Example:**
```python
import json

calculator = BiorhythmCalculator(days=14)
birthdate = datetime(1990, 5, 15)
data = calculator.generate_timeseries_json(birthdate)

# Pretty print JSON
print(json.dumps(data, indent=2))

# Access specific data
for entry in data["data"]:
    print(f"Date: {entry['date']}, Physical: {entry['physical']:.2f}")
```

##### `is_critical_day(physical: float, emotional: float, intellectual: float) -> Tuple[bool, List[str]]`

Determine if a day is considered "critical" (cycles near zero).

**Parameters:**
- `physical`: Physical cycle value (-1.0 to 1.0)
- `emotional`: Emotional cycle value (-1.0 to 1.0) 
- `intellectual`: Intellectual cycle value (-1.0 to 1.0)

**Returns:**
- Tuple of (is_critical: bool, critical_cycles: List[str])

**Example:**
```python
physical, emotional, intellectual = calculator.calculate_biorhythm_values(
    birthdate, target_date
)

is_critical, cycles = calculator.is_critical_day(physical, emotional, intellectual)

if is_critical:
    print(f"Critical day! Affected cycles: {', '.join(cycles)}")
```

### DateValidator

Static utility class for date validation and creation.

#### Methods

##### `validate_date_components(year: int, month: int, day: int) -> None`

Validate year, month, and day components.

**Raises:**
- `DateValidationError`: If any component is invalid

##### `create_validated_date(year: int, month: int, day: int) -> datetime`

Create a validated datetime object.

**Returns:**
- `datetime` object if valid

**Raises:**
- `DateValidationError`: If date is invalid or in the future

### UserInterface

Interactive command-line interface for user input.

#### Methods

##### `get_user_input() -> Tuple[int, int, int, str, int]`

Collect user input for birthdate, orientation, and chart parameters.

**Returns:**
- Tuple of (year, month, day, orientation, days)

## Exception Classes

### BiorhythmError

Base exception for biorhythm-related errors.

### DateValidationError

Raised when date validation fails.

### ChartParameterError

Raised when chart parameters are invalid.

## Constants

```python
PHYSICAL_CYCLE_DAYS = 23      # Physical cycle length
EMOTIONAL_CYCLE_DAYS = 28     # Emotional cycle length  
INTELLECTUAL_CYCLE_DAYS = 33  # Intellectual cycle length
MIN_CHART_WIDTH = 12          # Minimum chart width
DEFAULT_CHART_WIDTH = 55      # Default chart width
DEFAULT_DAYS_TO_PLOT = 29     # Default number of days
MIN_YEAR = 1                  # Minimum valid year
MAX_YEAR = 9999              # Maximum valid year
CRITICAL_DAY_THRESHOLD = 0.05 # Threshold for critical days
```

## Usage Examples

### Basic Chart Generation

```python
from biorythm.core import BiorhythmCalculator
from datetime import datetime

# Create calculator
calc = BiorhythmCalculator()

# Generate chart for someone born May 15, 1990
birthdate = datetime(1990, 5, 15)
calc.generate_chart(birthdate)
```

### Horizontal Timeline Chart

```python
# Create horizontal timeline chart
calc = BiorhythmCalculator(
    width=80,
    days=30,
    orientation="horizontal"
)

calc.generate_chart(birthdate)
```

### JSON Data Export

```python
# Generate data for API or analysis
data = calc.generate_timeseries_json(birthdate)

# Access metadata
print(f"Days alive: {data['meta']['days_alive']}")
print(f"Critical days: {len(data['critical_days'])}")

# Process timeseries data
for entry in data["data"]:
    if entry["critical_cycles"]:
        print(f"Critical day {entry['date']}: {entry['critical_cycles']}")
```

### Custom Parameters

```python
# Large chart for detailed view
calc = BiorhythmCalculator(
    width=120,  # Wide chart
    days=60,    # 2 months of data
    orientation="vertical"
)

calc.generate_chart(birthdate)
```

## Scientific Disclaimer

⚠️ **Important:** Biorhythm theory is considered pseudoscience with no scientific evidence supporting its claims. This implementation is provided for educational and entertainment purposes only. Multiple peer-reviewed studies have found no correlation between biorhythm cycles and human performance beyond random chance.

## See Also

- [Calculator API](calculator.md) - High-level calculator interface
- [JSON Schema](json-schema.md) - JSON output format specification
- [Usage Examples](../user-guide/usage-examples.md) - Practical usage scenarios