# Output Formats

PyBiorythm supports multiple output formats to suit different use cases, from simple visualization to data analysis.

## Chart Formats

### Vertical Chart (Default)

The traditional biorhythm chart format with time flowing top-to-bottom:

```bash
python main.py -y 1990 -m 5 -d 15 --orientation vertical
```

**Example Output:**
```
=== BIORHYTHM CHART ===
Birth Date: 1990-05-15
Chart Date: 2025-08-07 (12837 days alive)

⚠️  SCIENTIFIC WARNING ⚠️
Biorhythm theory is PSEUDOSCIENCE with no proven validity!
Use for entertainment and educational purposes only.

Key: Physical (p), Emotional (e), Intellectual (i)
Critical days marked when cycles cross zero line (:)

Thu Aug  7    p     :     e i    
Fri Aug  8       p  :  e      i  
Sat Aug  9          : p    e   i 
Sun Aug 10          :   p     e i
Mon Aug 11          :      p e  i
Tue Aug 12          :       p e i
Wed Aug 13      p   :        e i
Thu Aug 14   p      :         ei
```

**Features:**
- ✅ Easy to read date-by-date
- ✅ Clear critical day identification  
- ✅ Compact representation
- ✅ Traditional format users expect

### Horizontal Chart (Timeline)

Wave-like visualization with time flowing left-to-right:

```bash
python main.py -y 1990 -m 5 -d 15 --orientation horizontal
```

**Example Output:**
```
=== BIORHYTHM WAVE (Physical + Emotional + Intellectual) ===

                    e               
            p               i       
                        e           
      p                     i       
                e                   
 p                           i      
                    e               
                                i   
```

**Features:**
- ✅ Wave pattern visualization
- ✅ Shows cycle relationships
- ✅ Good for trend analysis
- ✅ Compact for long periods

## JSON Formats

### JSON Vertical

Structured data with vertical chart metadata:

```bash
python main.py -y 1990 -m 5 -d 15 --orientation json-vertical
```

### JSON Horizontal

Structured data with horizontal chart metadata:

```bash
python main.py -y 1990 -m 5 -d 15 --orientation json-horizontal
```

## JSON Schema Reference

Both JSON formats follow the same schema with different metadata:

```json
{
  "meta": {
    "generator": "biorythm",
    "version": "1.2.1",
    "birthdate": "1990-05-15",
    "plot_date": "2025-08-07", 
    "days_alive": 12837,
    "cycle_lengths_days": {
      "physical": 23,
      "emotional": 28,
      "intellectual": 33
    },
    "chart_orientation": "vertical",
    "days": 29,
    "width": 55,
    "scientific_warning": "⚠️ SCIENTIFIC WARNING ⚠️..."
  },
  "cycle_repeats": {
    "physical_emotional_repeat_in_days": 644,
    "all_cycles_repeat_in_days": 21252
  },
  "critical_days": [
    {
      "date": "2025-08-05",
      "cycles": "Physical cycle(s) near zero"
    }
  ],
  "data": [
    {
      "date": "2025-07-24",
      "days_alive": 12823,
      "physical": -0.8987940462991669,
      "emotional": 0.9744583088414919,
      "intellectual": -0.9510565162951536,
      "critical_cycles": []
    }
  ]
}
```

## Metadata Fields

### Meta Section

| Field | Type | Description |
|-------|------|-------------|
| `generator` | string | Software identifier |
| `version` | string | Software version |
| `birthdate` | string | Birth date (ISO format) |
| `plot_date` | string | Chart start date (ISO format) |
| `days_alive` | integer | Days between birth and plot date |
| `cycle_lengths_days` | object | Standard cycle lengths |
| `chart_orientation` | string | Chart type metadata |
| `days` | integer | Number of days in dataset |
| `width` | integer | Chart width (characters) |
| `scientific_warning` | string | Pseudoscience disclaimer |

### Cycle Repeats

| Field | Type | Description |
|-------|------|-------------|
| `physical_emotional_repeat_in_days` | integer | When P+E cycles repeat (644 days) |
| `all_cycles_repeat_in_days` | integer | When all cycles repeat (21,252 days) |

### Critical Days

Array of critical day events:

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date of critical event |
| `cycles` | string | Which cycle(s) are critical |

### Data Points

Each data point contains:

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `date` | string | | Date (ISO format) |
| `days_alive` | integer | 0+ | Days since birth |
| `physical` | float | -1.0 to +1.0 | Physical cycle value |
| `emotional` | float | -1.0 to +1.0 | Emotional cycle value |
| `intellectual` | float | -1.0 to +1.0 | Intellectual cycle value |
| `critical_cycles` | array | | List of cycles near zero |

## Use Cases by Format

### ASCII Charts

**Best for:**
- ✅ Quick visual reference
- ✅ Terminal/console applications
- ✅ Email or text-based reports
- ✅ Debugging and development
- ✅ Traditional biorhythm users

**Examples:**
```bash
# Daily check
python main.py -y 1990 -m 5 -d 15 --days 7

# Monthly overview  
python main.py -y 1990 -m 5 -d 15 --days 30 --orientation horizontal

# Extended analysis
python main.py -y 1990 -m 5 -d 15 --days 90
```

### JSON Data

**Best for:**
- ✅ Data analysis and visualization
- ✅ Machine learning training data
- ✅ API integrations
- ✅ Statistical analysis
- ✅ Custom application development

**Examples:**
```python
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = json.loads(json_output)
df = pd.DataFrame(data['data'])

# Analysis
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Visualization
df[['physical', 'emotional', 'intellectual']].plot(figsize=(12, 6))
plt.title('Biorhythm Cycles Over Time')
plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)
plt.show()
```

## Output Customization

### Chart Size

```bash
# Narrow chart (minimum width: 12)
python main.py -y 1990 -m 5 -d 15 --orientation vertical  # Default width: 55

# Wide chart (programmatic)
calc = BiorhythmCalculator(width=100)
```

### Time Period

```bash
# One week
python main.py -y 1990 -m 5 -d 15 --days 7

# One month  
python main.py -y 1990 -m 5 -d 15 --days 30

# One year (JSON recommended for large datasets)
python main.py -y 1990 -m 5 -d 15 --days 365 --orientation json-vertical
```

## File Output

### Save to File

```bash
# ASCII chart to file
python main.py -y 1990 -m 5 -d 15 > biorhythm_chart.txt

# JSON data to file
python main.py -y 1990 -m 5 -d 15 --orientation json-vertical > data.json

# Multiple formats
python main.py -y 1990 -m 5 -d 15 --orientation vertical > chart.txt
python main.py -y 1990 -m 5 -d 15 --orientation json-vertical > data.json
```

### Batch Processing

```bash
#!/bin/bash
# Generate multiple formats for analysis

birthdate="1990-05-15"
IFS='-' read -r year month day <<< "$birthdate"

# Generate all formats
python main.py -y "$year" -m "$month" -d "$day" --orientation vertical > "${birthdate}_chart.txt"
python main.py -y "$year" -m "$month" -d "$day" --orientation horizontal > "${birthdate}_wave.txt"  
python main.py -y "$year" -m "$month" -d "$day" --orientation json-vertical > "${birthdate}_data.json"
```

## Integration Examples

### Pandas Analysis

```python
import pandas as pd
import json

# Load JSON data
with open('biorhythm_data.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data['data'])
df['date'] = pd.to_datetime(df['date'])

# Statistical analysis
stats = df[['physical', 'emotional', 'intellectual']].describe()
correlation = df[['physical', 'emotional', 'intellectual']].corr()

print("Descriptive Statistics:")
print(stats)
print("\nCorrelation Matrix:")
print(correlation)
```

### Web API Integration

```python
from flask import Flask, jsonify
from biorythm import BiorhythmCalculator
from datetime import datetime

app = Flask(__name__)

@app.route('/biorhythm/<int:year>/<int:month>/<int:day>')
def get_biorhythm(year, month, day):
    calc = BiorhythmCalculator(days=30)
    birthdate = datetime(year, month, day)
    json_data = calc.generate_timeseries_json(birthdate)
    
    return jsonify(json.loads(json_data))

if __name__ == '__main__':
    app.run(debug=True)
```

### Visualization

```python
import matplotlib.pyplot as plt
import numpy as np

# Custom plotting function
def plot_biorhythm(json_data):
    data = json.loads(json_data)
    df = pd.DataFrame(data['data'])
    
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Plot cycles
    ax.plot(df['date'], df['physical'], 'r-', label='Physical (23d)', linewidth=2)
    ax.plot(df['date'], df['emotional'], 'b-', label='Emotional (28d)', linewidth=2)
    ax.plot(df['date'], df['intellectual'], 'g-', label='Intellectual (33d)', linewidth=2)
    
    # Mark critical days
    critical_dates = [cd['date'] for cd in data['critical_days']]
    for date in critical_dates:
        ax.axvline(pd.to_datetime(date), color='orange', linestyle='--', alpha=0.7)
    
    # Formatting
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax.set_ylim(-1.1, 1.1)
    ax.set_ylabel('Cycle Value')
    ax.set_title(f'Biorhythm Chart - Born {data["meta"]["birthdate"]}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
```

## Performance Considerations

| Format | Speed | Memory | Best for |
|--------|-------|---------|----------|
| **Vertical ASCII** | Fastest | Lowest | Quick checks, small periods |
| **Horizontal ASCII** | Fast | Low | Trend visualization, medium periods |
| **JSON** | Medium | Medium | Data analysis, large periods |
| **JSON + Pandas** | Slower | Higher | Statistical analysis, visualization |

## Next Steps

- **Learn CLI usage**: [Command Line Interface](cli.md)
- **See more examples**: [Usage Examples](usage-examples.md)  
- **API integration**: [Calculator API](../api/calculator.md)
- **Data analysis**: [JSON Schema](../api/json-schema.md)