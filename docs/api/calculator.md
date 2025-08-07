# BiorhythmCalculator API Reference

The `BiorhythmCalculator` class is the main interface for generating biorhythm calculations and visualizations.

## Class: BiorhythmCalculator

```python
from biorythm import BiorhythmCalculator
```

### Constructor

```python
BiorhythmCalculator(width=55, days=29, orientation="vertical")
```

**Parameters:**

- `width` (int, optional): Chart width in characters. Minimum 12. Default: 55
- `days` (int, optional): Number of days to plot. Default: 29  
- `orientation` (str, optional): Chart orientation. Options: "vertical", "horizontal". Default: "vertical"

**Raises:**

- `ValueError`: If width < 12 or orientation is invalid

**Example:**
```python
# Default calculator
calc = BiorhythmCalculator()

# Custom configuration
calc = BiorhythmCalculator(width=80, days=60, orientation="horizontal")
```

## Methods

### generate_chart()

Generate and print ASCII biorhythm chart to stdout.

```python
generate_chart(birthdate: datetime, plot_date: datetime = None) -> None
```

**Parameters:**

- `birthdate` (datetime): The person's birth date
- `plot_date` (datetime, optional): Starting date for chart. Defaults to today

**Raises:**

- `ValueError`: If birthdate is in the future or invalid
- `TypeError`: If birthdate is not a datetime object

**Example:**
```python
from datetime import datetime

calc = BiorhythmCalculator()
birthdate = datetime(1990, 5, 15)

# Chart starting from today
calc.generate_chart(birthdate)

# Chart starting from specific date
plot_date = datetime(2025, 1, 1)
calc.generate_chart(birthdate, plot_date)
```

**Output:**
```
=== BIORHYTHM CHART ===
Birth Date: 1990-05-15
Chart Date: 2025-08-07 (12837 days alive)

Thu Aug  7    p     :     e i    
Fri Aug  8       p  :  e      i  
Sat Aug  9          : p    e   i 
```

### generate_timeseries_json()

Generate JSON payload with biorhythm timeseries data and metadata.

```python
generate_timeseries_json(
    birthdate: datetime, 
    plot_date: datetime = None,
    chart_orientation: str = "vertical"
) -> str
```

**Parameters:**

- `birthdate` (datetime): The person's birth date
- `plot_date` (datetime, optional): Starting date for data. Defaults to today  
- `chart_orientation` (str, optional): Metadata orientation. Default: "vertical"

**Returns:**

- `str`: JSON string with timeseries data and metadata

**Raises:**

- `ValueError`: If birthdate is in the future or invalid
- `TypeError`: If birthdate is not a datetime object

**Example:**
```python
import json

calc = BiorhythmCalculator(days=7)
birthdate = datetime(1990, 5, 15)

# Generate JSON data
json_str = calc.generate_timeseries_json(birthdate)
data = json.loads(json_str)

# Access data
print(f"Days alive: {data['meta']['days_alive']}")
print(f"Physical cycle: {data['data'][0]['physical']}")
```

**JSON Schema:**
```json
{
  "meta": {
    "generator": "string",
    "version": "string", 
    "birthdate": "YYYY-MM-DD",
    "plot_date": "YYYY-MM-DD",
    "days_alive": "integer",
    "cycle_lengths_days": {
      "physical": 23,
      "emotional": 28,
      "intellectual": 33
    },
    "chart_orientation": "string",
    "days": "integer",
    "width": "integer",
    "scientific_warning": "string"
  },
  "cycle_repeats": {
    "physical_emotional_repeat_in_days": "integer",
    "all_cycles_repeat_in_days": "integer"
  },
  "critical_days": [
    {
      "date": "YYYY-MM-DD",
      "cycles": "string"
    }
  ],
  "data": [
    {
      "date": "YYYY-MM-DD", 
      "days_alive": "integer",
      "physical": "float",
      "emotional": "float", 
      "intellectual": "float",
      "critical_cycles": ["string"]
    }
  ]
}
```

### calculate_biorhythm_values()

Calculate raw biorhythm cycle values for a specific date.

```python
calculate_biorhythm_values(birthdate: datetime, target_date: datetime) -> tuple[float, float, float]
```

**Parameters:**

- `birthdate` (datetime): The person's birth date
- `target_date` (datetime): Date to calculate cycles for

**Returns:**

- `tuple[float, float, float]`: (physical, emotional, intellectual) values between -1.0 and +1.0

**Raises:**

- `ValueError`: If birthdate is after target_date
- `TypeError`: If dates are not datetime objects

**Example:**
```python
calc = BiorhythmCalculator()
birthdate = datetime(1990, 5, 15)
target_date = datetime(2025, 8, 7)

physical, emotional, intellectual = calc.calculate_biorhythm_values(birthdate, target_date)

print(f"Physical: {physical:.3f}")      # e.g., -0.899
print(f"Emotional: {emotional:.3f}")    # e.g., 0.974
print(f"Intellectual: {intellectual:.3f}") # e.g., -0.951
```

## Properties

### width
```python
@property
def width(self) -> int
```
Get the chart width in characters.

### days  
```python
@property
def days(self) -> int
```
Get the number of days to plot.

### orientation
```python
@property 
def orientation(self) -> str
```
Get the chart orientation ("vertical" or "horizontal").

## Class Constants

### Cycle Lengths
```python
PHYSICAL_CYCLE = 23     # Physical cycle length in days
EMOTIONAL_CYCLE = 28    # Emotional cycle length in days  
INTELLECTUAL_CYCLE = 33 # Intellectual cycle length in days
```

### Critical Threshold
```python
CRITICAL_THRESHOLD = 0.1  # Threshold for critical day detection
```

## Usage Patterns

### Basic Usage
```python
from datetime import datetime
from biorythm import BiorhythmCalculator

# Simple chart generation
calc = BiorhythmCalculator()
calc.generate_chart(datetime(1990, 5, 15))
```

### Data Analysis
```python
import json
import pandas as pd

# Generate full year of data
calc = BiorhythmCalculator(days=365)
json_data = calc.generate_timeseries_json(datetime(1990, 5, 15))

# Convert to pandas DataFrame
data = json.loads(json_data)
df = pd.DataFrame(data['data'])
df['date'] = pd.to_datetime(df['date'])

# Analyze patterns
correlation = df[['physical', 'emotional', 'intellectual']].corr()
print(correlation)
```

### Custom Visualization
```python
import matplotlib.pyplot as plt

# Get raw data points
calc = BiorhythmCalculator(days=90)
birthdate = datetime(1990, 5, 15)

dates = []
physical = []
emotional = []
intellectual = []

for i in range(90):
    target_date = datetime.now() + timedelta(days=i)
    p, e, i_val = calc.calculate_biorhythm_values(birthdate, target_date)
    
    dates.append(target_date)
    physical.append(p)
    emotional.append(e) 
    intellectual.append(i_val)

# Plot custom chart
plt.figure(figsize=(12, 6))
plt.plot(dates, physical, label='Physical (23d)', color='red')
plt.plot(dates, emotional, label='Emotional (28d)', color='blue')
plt.plot(dates, intellectual, label='Intellectual (33d)', color='green')
plt.legend()
plt.show()
```

## Error Handling

```python
from datetime import datetime
from biorythm import BiorhythmCalculator

calc = BiorhythmCalculator()

try:
    # This will raise ValueError - future date
    calc.generate_chart(datetime(2030, 1, 1))
except ValueError as e:
    print(f"Date error: {e}")

try:
    # This will raise ValueError - invalid width
    calc = BiorhythmCalculator(width=5)
except ValueError as e:
    print(f"Configuration error: {e}")

try:
    # This will raise TypeError - wrong type
    calc.generate_chart("1990-05-15")
except TypeError as e:
    print(f"Type error: {e}")
```

## Thread Safety

The `BiorhythmCalculator` class is thread-safe for read operations. Multiple threads can safely call calculation methods simultaneously on the same instance.

```python
import threading
from concurrent.futures import ThreadPoolExecutor

def calculate_for_person(birthdate):
    calc = BiorhythmCalculator()
    return calc.generate_timeseries_json(birthdate)

birthdates = [
    datetime(1980, 1, 1),
    datetime(1990, 5, 15), 
    datetime(2000, 12, 31)
]

# Safe concurrent execution
with ThreadPoolExecutor() as executor:
    results = list(executor.map(calculate_for_person, birthdates))
```