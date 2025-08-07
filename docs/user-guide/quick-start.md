# Quick Start Guide

Get up and running with PyBiorythm in just a few minutes!

## Installation

Choose your preferred installation method:

=== "uv (Recommended)"
    ```bash
    # Using uv package manager
    uv add biorythm

    # Or from source
    git clone https://github.com/dkdndes/pybiorythm.git
    cd pybiorythm  
    uv pip install -e .
    ```

=== "pip"
    ```bash
    # Install from PyPI (when published)
    pip install biorythm

    # Or from source
    git clone https://github.com/dkdndes/pybiorythm.git
    cd pybiorythm
    pip install .
    ```

=== "Docker"
    ```bash
    # Pull and run (easiest option)
    docker run -it biorythm:latest

    # Or build locally
    git clone https://github.com/dkdndes/pybiorythm.git
    cd pybiorythm
    docker build -t biorythm:latest .
    docker run -it biorythm:latest
    ```

## Your First Biorhythm Chart

### Interactive Mode

The simplest way to get started:

```bash
python main.py
```

You'll be prompted to enter:
- Birth year (1-9999)
- Birth month (1-12)  
- Birth day (1-31)

### Command Line Mode

For quick calculations:

```bash
# Basic chart for someone born May 15, 1990
python main.py -y 1990 -m 5 -d 15

# Horizontal timeline view
python main.py -y 1990 -m 5 -d 15 --orientation horizontal

# Extended period (60 days instead of default 29)
python main.py -y 1990 -m 5 -d 15 --days 60
```

### Programmatic Usage

```python
from datetime import datetime
from biorythm import BiorhythmCalculator

# Create calculator instance
calc = BiorhythmCalculator(
    width=60,           # Chart width in characters
    days=30,           # Number of days to plot
    orientation="vertical"  # "vertical" or "horizontal"
)

# Generate chart for birthdate
birthdate = datetime(1990, 5, 15)
calc.generate_chart(birthdate)
```

## Understanding the Output

### Vertical Chart (Default)

```
Mon May 15    p     :     e i    
Tue May 16       p  :  e      i  
Wed May 17          : p    e   i 
Thu May 18          :   p     e i
Fri May 19          :      p e  i
```

- **p** = Physical cycle (23 days)
- **e** = Emotional cycle (28 days)
- **i** = Intellectual cycle (33 days)
- **:** = Zero line (critical days when cycles cross)

### Chart Interpretation

- **Left side of :** = Negative phase (low energy, recovery)
- **Right side of :** = Positive phase (high energy, peak performance)
- **Near the :** = Critical days (transitions, potential instability)

## JSON Output for Data Analysis

Generate structured data perfect for analysis:

```python
# Generate JSON timeseries data
json_data = calc.generate_timeseries_json(birthdate)

# The JSON includes:
# - Raw cycle values (-1.0 to +1.0)
# - Date information
# - Critical day detection
# - Metadata for analysis
```

Example JSON structure:

```json
{
  "meta": {
    "birthdate": "1990-05-15",
    "days_alive": 12837,
    "cycle_lengths_days": {
      "physical": 23,
      "emotional": 28, 
      "intellectual": 33
    }
  },
  "data": [
    {
      "date": "2025-07-24",
      "physical": -0.899,
      "emotional": 0.974,
      "intellectual": -0.951,
      "critical_cycles": []
    }
  ]
}
```

## Common Use Cases

### 1. Personal Entertainment

Generate your daily biorhythm chart:

```bash
# Today's chart
python main.py -y YOUR_BIRTH_YEAR -m YOUR_BIRTH_MONTH -d YOUR_BIRTH_DAY
```

### 2. Data Analysis

```python
import json
import pandas as pd
from biorythm import BiorhythmCalculator

calc = BiorhythmCalculator(days=365)  # Full year of data
data = calc.generate_timeseries_json(datetime(1990, 5, 15))

# Convert to pandas DataFrame
df = pd.DataFrame(data['data'])
df['date'] = pd.to_datetime(df['date'])

# Analyze patterns
print(df[['physical', 'emotional', 'intellectual']].describe())
```

### 3. Testing Data Generation

```python
# Generate mock data for testing your analytics pipeline
test_birthdates = [
    datetime(1980, 1, 1),
    datetime(1990, 6, 15),
    datetime(2000, 12, 31)
]

for birthdate in test_birthdates:
    data = calc.generate_timeseries_json(birthdate)
    # Use data for testing your pipeline
```

## Next Steps

- **Learn more about output formats**: [Output Formats](output-formats.md)
- **Explore command line options**: [CLI Reference](cli.md)
- **See more examples**: [Usage Examples](usage-examples.md)
- **Set up development**: [Developer Guide](../developer-guide/setup.md)

!!! tip "Remember"
    Biorhythm theory is pseudoscience with no scientific validity. Use this for entertainment, education, and testing purposes only!