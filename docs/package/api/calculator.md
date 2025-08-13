# BiorhythmCalculator API Reference

The `BiorhythmCalculator` class is the main interface for generating biorhythm calculations and visualizations in your Python applications.

## Quick Example

```python
from datetime import datetime
from biorythm import BiorhythmCalculator

# Create calculator
calc = BiorhythmCalculator(width=60, days=30)

# Generate chart for someone born May 15, 1990
birthdate = datetime(1990, 5, 15)
calc.generate_chart(birthdate)

# Get JSON data for analysis
data = calc.generate_timeseries_json(birthdate)
```

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

**Examples:**

```python
# Default calculator
calc = BiorhythmCalculator()

# Custom wide chart for 60 days
calc = BiorhythmCalculator(width=80, days=60)

# Horizontal timeline view
calc = BiorhythmCalculator(orientation="horizontal")
```

## Methods

### generate_chart()

Generate and print ASCII biorhythm chart to stdout.

```python
generate_chart(birthdate, plot_date=None)
```

**Parameters:**

- `birthdate` (datetime): Birth date for biorhythm calculation
- `plot_date` (datetime, optional): Starting date for chart. Default: today

**Returns:** None (prints to stdout)

**Example:**

```python
from datetime import datetime
calc = BiorhythmCalculator()
calc.generate_chart(datetime(1990, 5, 15))
```

**Output:**
```
Mon May 15    p     :     e i    
Tue May 16       p  :  e      i  
Wed May 17          : p    e   i 
```

### generate_timeseries_json()

Generate structured JSON data with biorhythm timeseries and metadata.

```python
generate_timeseries_json(birthdate, plot_date=None, chart_orientation="vertical")
```

**Parameters:**

- `birthdate` (datetime): Birth date for biorhythm calculation
- `plot_date` (datetime, optional): Starting date for timeseries. Default: today
- `chart_orientation` (str, optional): Chart type for metadata. Default: "vertical"

**Returns:** dict - Complete JSON payload with metadata and timeseries data

**Example:**

```python
data = calc.generate_timeseries_json(datetime(1990, 5, 15))
print(data.keys())  # ['metadata', 'timeseries']

# Access timeseries data
for entry in data['timeseries']:
    date = entry['date']
    physical = entry['cycles']['physical']
    print(f"{date}: Physical = {physical:.2f}")
```

**JSON Structure:**

```json
{
  "metadata": {
    "birthdate": "1990-05-15",
    "chart_period_days": 30,
    "cycles": {
      "physical": {"period_days": 23},
      "emotional": {"period_days": 28}, 
      "intellectual": {"period_days": 33}
    }
  },
  "timeseries": [
    {
      "date": "2024-01-15",
      "day_number": 12345,
      "cycles": {
        "physical": 0.78,
        "emotional": -0.43,
        "intellectual": 0.21
      },
      "critical_days": []
    }
  ]
}
```

### calculate_biorhythm_values()

Calculate raw biorhythm cycle values for a specific date.

```python
calculate_biorhythm_values(birthdate, target_date)
```

**Parameters:**

- `birthdate` (datetime): Birth date for calculation
- `target_date` (datetime): Date to calculate values for

**Returns:** tuple - `(physical, emotional, intellectual)` values between -1.0 and +1.0

**Example:**

```python
from datetime import datetime
calc = BiorhythmCalculator()

physical, emotional, intellectual = calc.calculate_biorhythm_values(
    datetime(1990, 5, 15),  # birthdate
    datetime(2024, 1, 15)   # target date
)

print(f"Physical: {physical:.2f}")
print(f"Emotional: {emotional:.2f}")
print(f"Intellectual: {intellectual:.2f}")
```

## Integration with Data Analysis Libraries

### Pandas Integration

```python
import pandas as pd
from biorythm import BiorhythmCalculator

calc = BiorhythmCalculator(days=90)
data = calc.generate_timeseries_json(birthdate)

# Convert to DataFrame
df = pd.json_normalize(data['timeseries'])
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Rename columns for easier access
df.columns = ['day_number', 'physical', 'emotional', 'intellectual', 'critical_days']

# Analyze cycles
cycle_stats = df[['physical', 'emotional', 'intellectual']].describe()
print(cycle_stats)
```

### Matplotlib Visualization

```python
import matplotlib.pyplot as plt
import pandas as pd

# Get data as DataFrame (from above)
df = pd.json_normalize(data['timeseries'])
df['date'] = pd.to_datetime(df['date'])

# Plot all cycles
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['cycles.physical'], label='Physical (23 days)', linewidth=2)
plt.plot(df['date'], df['cycles.emotional'], label='Emotional (28 days)', linewidth=2)
plt.plot(df['date'], df['cycles.intellectual'], label='Intellectual (33 days)', linewidth=2)
plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)
plt.xlabel('Date')
plt.ylabel('Cycle Value')
plt.title('Biorhythm Cycles Over Time')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

## Error Handling

```python
from biorythm import BiorhythmCalculator
from datetime import datetime

try:
    # This will raise ValueError - width too small
    calc = BiorhythmCalculator(width=5)
except ValueError as e:
    print(f"Configuration error: {e}")

try:
    # This will raise ValueError - invalid orientation
    calc = BiorhythmCalculator(orientation="diagonal")
except ValueError as e:
    print(f"Configuration error: {e}")
```

## Performance Considerations

- **Memory usage**: Minimal - each timeseries entry is ~100 bytes
- **Calculation speed**: Very fast - O(n) where n is number of days
- **Recommended limits**: Up to 1000 days for responsive performance
- **JSON output size**: ~1KB per 10 days of data

```python
import time
from datetime import datetime

# Benchmark calculation for 365 days
calc = BiorhythmCalculator(days=365)
start_time = time.time()
data = calc.generate_timeseries_json(datetime(1990, 5, 15))
elapsed = time.time() - start_time

print(f"Generated 365 days of data in {elapsed:.3f} seconds")
print(f"Data points: {len(data['timeseries'])}")
```

## See Also

- **[Core Functions](core.md)** - Lower-level calculation functions
- **[JSON Schema](json-schema.md)** - Complete data format specification  
- **[Error Handling](errors.md)** - Exception types and handling
- **[Usage Examples](../guides/basic-usage.md)** - More integration examples
- **[Advanced Usage](../guides/advanced-usage.md)** - Configuration and customization