# Biorhythm Sample Datasets

This directory contains sample biorhythm datasets for analysis and experimentation.

## Quick Start

```python
import pandas as pd
import json

# Load JSON data
with open('one_year_1990.json', 'r') as f:
    data = json.load(f)

# Convert to pandas DataFrame
df = pd.json_normalize(data['timeseries'])
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Basic analysis
print(df.describe())
```

## Available Datasets

- `one_year_1990.json/csv` - One year analysis dataset
- `two_years_1985.json/csv` - Two year analysis dataset  
- `quarterly_1995.json/csv` - 90-day quarterly dataset
- `five_years_1980.json/csv` - Five year big data dataset
- `multiple_people_2024.json/csv` - Multi-person comparison dataset

## Documentation

See `data_dictionary.json` for complete field descriptions and analysis suggestions.

## Scientific Disclaimer

Biorhythm theory is considered pseudoscience. These datasets are provided for educational and entertainment purposes only.
