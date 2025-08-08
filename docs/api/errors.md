# Error Handling

PyBiorythm uses a structured exception hierarchy for comprehensive error handling.

## Exception Hierarchy

```python
BiorhythmError (base)
├── DateValidationError
├── ChartParameterError  
└── CalculationError
```

## Exception Classes

### BiorhythmError
**Base exception** for all biorhythm-related errors.

```python
class BiorhythmError(Exception):
    """Base exception for all biorhythm errors."""
    pass
```

### DateValidationError
**Date validation** errors for invalid dates or date ranges.

```python
class DateValidationError(BiorhythmError):
    """Raised for invalid date inputs."""
    pass
```

**Common scenarios:**
- Future birth dates
- Invalid calendar dates  
- Year out of range (1-9999)
- Invalid month/day values

### ChartParameterError
**Chart configuration** errors for invalid parameters.

```python
class ChartParameterError(BiorhythmError):
    """Raised for invalid chart parameters."""
    pass
```

**Common scenarios:**
- Chart width too small (< 12)
- Invalid orientation values
- Negative days parameter

### CalculationError
**Calculation** errors during biorhythm computation.

```python
class CalculationError(BiorhythmError):
    """Raised for calculation failures."""
    pass
```

## Error Handling Examples

### Date Validation
```python
from biorythm import BiorhythmCalculator, DateValidationError
from datetime import datetime

try:
    calc = BiorhythmCalculator()
    # Future date will raise error
    future_date = datetime(2030, 1, 1)
    result = calc.calculate_biorhythm_values(future_date, datetime.now())
except DateValidationError as e:
    print(f"Date error: {e}")
    # Handle invalid date
```

### Chart Parameters
```python
from biorythm import BiorhythmCalculator, ChartParameterError

try:
    # Width too small
    calc = BiorhythmCalculator(width=5)
except ChartParameterError as e:
    print(f"Parameter error: {e}")
    # Use default parameters
    calc = BiorhythmCalculator()
```

### Generic Error Handling
```python
from biorythm import BiorhythmCalculator, BiorhythmError

try:
    calc = BiorhythmCalculator()
    # ... operations
except BiorhythmError as e:
    print(f"Biorhythm error: {e}")
    # Handle any biorhythm-related error
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle other errors
```

## Best Practices

### 1. Specific Exception Handling
```python
# Good - specific handling
try:
    calc.generate_chart(birthdate)
except DateValidationError:
    # Handle date errors specifically
    show_date_input_form()
except ChartParameterError:
    # Handle parameter errors
    use_default_parameters()
```

### 2. Error Logging
```python
import logging

logger = logging.getLogger(__name__)

try:
    calc.generate_chart(birthdate)
except BiorhythmError as e:
    logger.error(f"Biorhythm calculation failed: {e}")
    raise
```

### 3. User-Friendly Messages
```python
try:
    calc = BiorhythmCalculator(width=user_width)
except ChartParameterError as e:
    # Convert technical error to user message
    print(f"Chart width must be at least 12 characters. Please try again.")
```

## Error Messages

### DateValidationError Messages
- `"Birth date cannot be in the future"`
- `"Year must be between 1 and 9999"`
- `"Invalid date: 2024-02-30"`
- `"Month must be between 1 and 12"`
- `"Day must be between 1 and 31"`

### ChartParameterError Messages  
- `"Chart width must be at least 12 characters"`
- `"Invalid orientation: must be 'vertical' or 'horizontal'"`
- `"Number of days must be positive"`

### CalculationError Messages
- `"Calculation failed for date range"`
- `"Mathematical overflow in cycle computation"`

---

**Related**: [Core API](core.md) | [Calculator API](calculator.md) | [JSON Schema](json-schema.md)