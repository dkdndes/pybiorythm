# Usage Examples

This page contains practical examples of using PyBiorythm for various scenarios.

## Basic Examples

### Generate Today's Chart

```python
from datetime import datetime
from biorythm import BiorhythmCalculator

# Create calculator and generate chart
calc = BiorhythmCalculator()
birthdate = datetime(1990, 5, 15)
calc.generate_chart(birthdate)
```

### Command Line Quick Start

```bash
# Interactive mode
python main.py

# Direct command
python main.py -y 1990 -m 5 -d 15
```

## Data Analysis Examples

### Monthly Analysis

```python
import json
import pandas as pd

# Generate 30 days of data
calc = BiorhythmCalculator(days=30)
json_data = calc.generate_timeseries_json(datetime(1990, 5, 15))
data = json.loads(json_data)

# Convert to DataFrame for analysis
df = pd.DataFrame(data['data'])
df['date'] = pd.to_datetime(df['date'])

# Find peak and low days
physical_peak = df.loc[df['physical'].idxmax()]
emotional_low = df.loc[df['emotional'].idxmin()]

print(f"Physical peak: {physical_peak['date']} ({physical_peak['physical']:.3f})")
print(f"Emotional low: {emotional_low['date']} ({emotional_low['emotional']:.3f})")
```

### Critical Days Detection

```python
# Identify critical days (cycles near zero)
critical_threshold = 0.1
critical_days = df[
    (abs(df['physical']) < critical_threshold) |
    (abs(df['emotional']) < critical_threshold) |
    (abs(df['intellectual']) < critical_threshold)
]

print("Critical days in the next 30 days:")
for _, day in critical_days.iterrows():
    cycles = []
    if abs(day['physical']) < critical_threshold:
        cycles.append('Physical')
    if abs(day['emotional']) < critical_threshold:
        cycles.append('Emotional')  
    if abs(day['intellectual']) < critical_threshold:
        cycles.append('Intellectual')
    
    print(f"{day['date'].strftime('%Y-%m-%d')}: {', '.join(cycles)}")
```

## More Examples Coming Soon

This documentation is being actively developed. More examples will be added covering:

- Docker usage scenarios
- Batch processing multiple birthdates
- Custom visualization with matplotlib
- Integration with web applications
- Statistical analysis patterns
- Performance optimization tips

## Contributing Examples

If you have useful examples to share, please contribute them via:
- [GitHub Issues](https://github.com/dkdndes/pybiorythm/issues)
- [Pull Requests](https://github.com/dkdndes/pybiorythm/pulls)

---

**Next**: [Command Line Interface](cli.md) | [Output Formats](output-formats.md)