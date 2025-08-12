# Core Functions API Reference

The `biorythm.core` module contains the underlying calculation functions used by `BiorhythmCalculator`. These functions can be used directly for custom implementations or integration with other systems.

## Module Import

```python
from biorythm.core import BiorhythmCalculator
# Or import specific functions
from biorythm.core import calculate_cycle_value, days_since_birth
```

## Core Calculation Functions

### calculate_cycle_value()

Calculate the value of a biorhythm cycle for a specific day.

```python
calculate_cycle_value(day_number, cycle_period)
```

**Parameters:**

- `day_number` (int): Number of days since birth
- `cycle_period` (int): Cycle period in days (23, 28, or 33)

**Returns:** float - Cycle value between -1.0 and +1.0

**Formula:** `sin(2π × day_number / cycle_period)`

**Example:**

```python
from biorythm.core import calculate_cycle_value

# Calculate physical cycle (23-day period) for day 100
physical_value = calculate_cycle_value(100, 23)
print(f"Physical cycle value: {physical_value:.3f}")

# Calculate all three cycles for day 100  
physical = calculate_cycle_value(100, 23)
emotional = calculate_cycle_value(100, 28)
intellectual = calculate_cycle_value(100, 33)

print(f"Day 100 - P:{physical:.3f} E:{emotional:.3f} I:{intellectual:.3f}")
```

### days_since_birth()

Calculate the number of days between birth date and target date.

```python
days_since_birth(birthdate, target_date)
```

**Parameters:**

- `birthdate` (datetime): Birth date
- `target_date` (datetime): Target date for calculation

**Returns:** int - Number of days (can be negative for dates before birth)

**Example:**

```python
from datetime import datetime
from biorythm.core import days_since_birth

birthdate = datetime(1990, 5, 15)
target_date = datetime(2024, 1, 15)

days = days_since_birth(birthdate, target_date)
print(f"Days since birth: {days}")  # Days since birth: 12298
```

### is_critical_day()

Determine if a given day is a critical day (cycle crosses zero).

```python
is_critical_day(day_number, cycle_period, tolerance=0.1)
```

**Parameters:**

- `day_number` (int): Number of days since birth
- `cycle_period` (int): Cycle period in days
- `tolerance` (float, optional): Tolerance for zero-crossing detection. Default: 0.1

**Returns:** str or None - Critical day type ("positive", "negative") or None

**Example:**

```python
from biorythm.core import is_critical_day

# Check if day 115 is a physical critical day
critical_type = is_critical_day(115, 23)
if critical_type:
    print(f"Day 115 is a physical critical day: {critical_type}")
else:
    print("Day 115 is not a physical critical day")
```

## Cycle Constants

The module defines standard biorhythm cycle periods:

```python
PHYSICAL_CYCLE = 23      # Physical cycle period
EMOTIONAL_CYCLE = 28     # Emotional cycle period  
INTELLECTUAL_CYCLE = 33  # Intellectual cycle period

# Example usage
from biorythm.core import PHYSICAL_CYCLE, calculate_cycle_value

physical_value = calculate_cycle_value(100, PHYSICAL_CYCLE)
```

## Advanced Usage Examples

### Custom Cycle Periods

```python
from biorythm.core import calculate_cycle_value

# Experiment with custom cycle periods
custom_cycles = {
    'creative': 37,      # Hypothetical creative cycle
    'intuitive': 43,     # Hypothetical intuitive cycle
    'social': 19         # Hypothetical social cycle
}

day_number = 200
for cycle_name, period in custom_cycles.items():
    value = calculate_cycle_value(day_number, period)
    print(f"{cycle_name.title()} ({period} days): {value:.3f}")
```

### Batch Calculation

```python
from datetime import datetime, timedelta
from biorythm.core import calculate_cycle_value, days_since_birth

def calculate_biorhythm_range(birthdate, start_date, num_days):
    """Calculate biorhythms for a range of days."""
    results = []
    
    for i in range(num_days):
        current_date = start_date + timedelta(days=i)
        day_number = days_since_birth(birthdate, current_date)
        
        values = {
            'date': current_date.strftime('%Y-%m-%d'),
            'physical': calculate_cycle_value(day_number, 23),
            'emotional': calculate_cycle_value(day_number, 28),
            'intellectual': calculate_cycle_value(day_number, 33)
        }
        results.append(values)
    
    return results

# Calculate 30 days of biorhythms
birthdate = datetime(1990, 5, 15)
start_date = datetime(2024, 1, 1)
biorhythms = calculate_biorhythm_range(birthdate, start_date, 30)

for entry in biorhythms[:5]:  # Show first 5 days
    print(f"{entry['date']}: P={entry['physical']:.3f} "
          f"E={entry['emotional']:.3f} I={entry['intellectual']:.3f}")
```

### Critical Day Detection

```python
from biorythm.core import calculate_cycle_value, is_critical_day

def find_critical_days(birthdate, start_date, num_days):
    """Find all critical days in a date range."""
    critical_days = []
    
    for i in range(num_days):
        current_date = start_date + timedelta(days=i)
        day_number = days_since_birth(birthdate, current_date)
        
        # Check each cycle for critical days
        cycles = [
            ('physical', 23),
            ('emotional', 28), 
            ('intellectual', 33)
        ]
        
        day_criticals = []
        for cycle_name, period in cycles:
            critical_type = is_critical_day(day_number, period)
            if critical_type:
                day_criticals.append(f"{cycle_name}_{critical_type}")
        
        if day_criticals:
            critical_days.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'critical_events': day_criticals
            })
    
    return critical_days

# Find critical days in January 2024
critical_days = find_critical_days(
    datetime(1990, 5, 15),
    datetime(2024, 1, 1), 
    31
)

print(f"Found {len(critical_days)} critical days in January:")
for day in critical_days:
    print(f"  {day['date']}: {', '.join(day['critical_events'])}")
```

### Performance Optimization

```python
import math
from typing import List, Tuple

def calculate_multiple_cycles_vectorized(day_numbers: List[int], 
                                       cycle_periods: List[int]) -> List[List[float]]:
    """Optimized calculation for multiple cycles and days."""
    results = []
    
    # Pre-calculate constants
    two_pi = 2.0 * math.pi
    period_constants = [two_pi / period for period in cycle_periods]
    
    for day_num in day_numbers:
        day_results = []
        for period_const in period_constants:
            value = math.sin(day_num * period_const)
            day_results.append(value)
        results.append(day_results)
    
    return results

# Example: Calculate 1000 days for all 3 cycles efficiently
day_numbers = list(range(1, 1001))
cycle_periods = [23, 28, 33]

import time
start_time = time.time()
results = calculate_multiple_cycles_vectorized(day_numbers, cycle_periods)
elapsed = time.time() - start_time

print(f"Calculated {len(day_numbers)} days × {len(cycle_periods)} cycles in {elapsed:.3f}s")
print(f"Rate: {len(day_numbers) * len(cycle_periods) / elapsed:.0f} calculations/second")
```

## Integration with NumPy

For high-performance calculations with large datasets:

```python
import numpy as np
from datetime import datetime, timedelta

def calculate_biorhythms_numpy(birthdate, start_date, num_days):
    """High-performance biorhythm calculation using NumPy."""
    
    # Create array of day numbers
    base_day = (start_date - birthdate).days
    day_numbers = np.arange(base_day, base_day + num_days)
    
    # Calculate cycles using vectorized operations
    physical = np.sin(2 * np.pi * day_numbers / 23)
    emotional = np.sin(2 * np.pi * day_numbers / 28)
    intellectual = np.sin(2 * np.pi * day_numbers / 33)
    
    # Create date array
    dates = np.array([start_date + timedelta(days=i) for i in range(num_days)])
    
    return {
        'dates': dates,
        'physical': physical,
        'emotional': emotional,
        'intellectual': intellectual
    }

# Example with 10,000 days
import time
birthdate = datetime(1990, 5, 15)
start_date = datetime(2024, 1, 1)

start_time = time.time()
results = calculate_biorhythms_numpy(birthdate, start_date, 10000)
elapsed = time.time() - start_time

print(f"NumPy calculation for 10,000 days: {elapsed:.3f}s")
print(f"Physical cycle stats: min={results['physical'].min():.3f}, "
      f"max={results['physical'].max():.3f}, mean={results['physical'].mean():.3f}")
```

## Mathematical Background

### Cycle Formula

The biorhythm calculation uses the sine function:

```
cycle_value = sin(2π × day_number / cycle_period)
```

Where:
- `day_number` = days since birth
- `cycle_period` = 23 (physical), 28 (emotional), or 33 (intellectual)

### Critical Days

Critical days occur when the cycle value is approximately zero, indicating a transition between positive and negative phases. The direction of crossing determines the type:

- **Positive critical day**: Cycle crosses from negative to positive (ascending)
- **Negative critical day**: Cycle crosses from positive to negative (descending)

### Cycle Relationships

The three standard cycles create complex interaction patterns:

- **Physical-Emotional repeat**: Every 644 days (23 × 28)
- **All cycles repeat**: Every 21,252 days (~58.2 years) (23 × 28 × 33)

## Error Handling

The core functions include basic validation:

```python
from biorythm.core import calculate_cycle_value

try:
    # Invalid cycle period
    value = calculate_cycle_value(100, 0)
except ValueError as e:
    print(f"Error: {e}")  # Error: Cycle period must be positive

try:
    # Very large day number (potential overflow)
    value = calculate_cycle_value(10**10, 23)
    print(f"Large day calculation: {value:.3f}")
except OverflowError as e:
    print(f"Calculation overflow: {e}")
```

## See Also

- **[BiorhythmCalculator API](calculator.md)** - High-level interface using these functions
- **[JSON Schema](json-schema.md)** - Data format for structured output
- **[Error Handling](errors.md)** - Exception types and handling
- **[Performance Guide](../reference/performance.md)** - Optimization techniques
- **[Integration Examples](../guides/integration.md)** - Using with scientific libraries