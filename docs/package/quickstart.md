# PyBiorythm Quickstart Guide

Get started with PyBiorythm in your Python applications in just 5 minutes! This guide focuses on integrating biorhythm calculations into your code for data analysis, visualization, or application features.

!!! warning "Scientific Disclaimer"
    Biorhythm theory is considered pseudoscience. This library is for entertainment and educational purposes only.

## 1. Installation (30 seconds)

Choose your preferred Python package manager:

=== "pip (Most Common)"
    ```bash
    pip install biorythm
    ```

=== "uv (Fastest)"
    ```bash
    uv add biorythm
    ```

=== "From Source"
    ```bash
    git clone https://github.com/dkdndes/pybiorythm.git
    cd pybiorythm
    pip install -e .
    ```

## 2. Basic Usage (60 seconds)

### Simple Chart Generation

```python
from datetime import datetime
from biorythm import BiorhythmCalculator

# Create calculator for someone born May 15, 1990
calc = BiorhythmCalculator(width=60, days=30)
birthdate = datetime(1990, 5, 15)

# Generate ASCII chart
calc.generate_chart(birthdate)
```

**Output:**
```
Mon Jan 15    p     :     e i    
Tue Jan 16       p  :  e      i  
Wed Jan 17          : p    e   i 
Thu Jan 18             p:      e i
...
```

### Get Data for Analysis

```python
# Get structured JSON data
data = calc.generate_timeseries_json(birthdate)

print(f"Generated {len(data['timeseries'])} days of data")
print(f"Cycles: {list(data['metadata']['cycles'].keys())}")

# Access individual values
first_day = data['timeseries'][0]
print(f"Date: {first_day['date']}")
print(f"Physical: {first_day['cycles']['physical']:.3f}")
print(f"Emotional: {first_day['cycles']['emotional']:.3f}")
print(f"Intellectual: {first_day['cycles']['intellectual']:.3f}")
```

## 3. Data Analysis Integration (2 minutes)

### With Pandas

Perfect for data scientists and analysts:

```python
import pandas as pd
from biorythm import BiorhythmCalculator

# Generate 90 days of biorhythm data
calc = BiorhythmCalculator(days=90)
data = calc.generate_timeseries_json(datetime(1990, 5, 15))

# Convert to pandas DataFrame
df = pd.json_normalize(data['timeseries'])
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Quick analysis
print("Cycle Statistics:")
cycle_cols = ['cycles.physical', 'cycles.emotional', 'cycles.intellectual']
print(df[cycle_cols].describe())

# Find critical days (cycle crossings)
critical_days = df[df['critical_days'].str.len() > 0]
print(f"\nFound {len(critical_days)} critical days")
```

### With Matplotlib

Visualize the cycles:

```python
import matplotlib.pyplot as plt

# Plot all three cycles
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df.index, df['cycles.physical'], 
        label='Physical (23 days)', linewidth=2, color='red')
ax.plot(df.index, df['cycles.emotional'], 
        label='Emotional (28 days)', linewidth=2, color='blue')
ax.plot(df.index, df['cycles.intellectual'], 
        label='Intellectual (33 days)', linewidth=2, color='green')

# Add zero line and formatting
ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
ax.set_xlabel('Date')
ax.set_ylabel('Cycle Value')
ax.set_title('Biorhythm Cycles Over Time')
ax.legend()
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## 4. Common Use Cases (2 minutes)

### Application Integration

```python
def get_user_biorhythm(user_birthdate, target_date=None):
    """Get biorhythm data for a user on a specific date."""
    if target_date is None:
        target_date = datetime.now()
    
    calc = BiorhythmCalculator()
    physical, emotional, intellectual = calc.calculate_biorhythm_values(
        user_birthdate, target_date
    )
    
    return {
        'date': target_date.strftime('%Y-%m-%d'),
        'physical': round(physical, 3),
        'emotional': round(emotional, 3),
        'intellectual': round(intellectual, 3),
        'summary': get_cycle_summary(physical, emotional, intellectual)
    }

def get_cycle_summary(physical, emotional, intellectual):
    """Generate a human-readable summary."""
    def describe_cycle(value):
        if value > 0.5: return "High"
        elif value > 0: return "Rising"
        elif value > -0.5: return "Falling"
        else: return "Low"
    
    return {
        'physical': describe_cycle(physical),
        'emotional': describe_cycle(emotional),
        'intellectual': describe_cycle(intellectual)
    }

# Example usage
user_birth = datetime(1985, 3, 22)
today_biorhythm = get_user_biorhythm(user_birth)
print(today_biorhythm)
```

### Batch Processing

```python
def analyze_biorhythm_period(birthdate, start_date, days=30):
    """Analyze biorhythm patterns over a period."""
    calc = BiorhythmCalculator(days=days)
    data = calc.generate_timeseries_json(birthdate, start_date)
    
    # Convert to DataFrame for analysis
    df = pd.json_normalize(data['timeseries'])
    
    # Calculate statistics
    stats = {
        'period_days': days,
        'critical_days': len(df[df['critical_days'].str.len() > 0]),
        'avg_physical': df['cycles.physical'].mean(),
        'avg_emotional': df['cycles.emotional'].mean(),
        'avg_intellectual': df['cycles.intellectual'].mean(),
        'physical_peaks': len(df[df['cycles.physical'] > 0.9]),
        'emotional_peaks': len(df[df['cycles.emotional'] > 0.9]),
        'intellectual_peaks': len(df[df['cycles.intellectual'] > 0.9])
    }
    
    return stats, df

# Analyze January 2024
stats, df = analyze_biorhythm_period(
    datetime(1990, 5, 15),
    datetime(2024, 1, 1),
    31
)

print("January 2024 Analysis:")
for key, value in stats.items():
    print(f"  {key}: {value}")
```

### Web API Integration

```python
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

@app.route('/biorhythm', methods=['GET'])
def get_biorhythm():
    """REST API endpoint for biorhythm data."""
    try:
        # Parse parameters
        birthdate_str = request.args.get('birthdate')  # Format: YYYY-MM-DD
        days = int(request.args.get('days', 30))
        
        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d')
        
        # Generate biorhythm data
        calc = BiorhythmCalculator(days=days)
        data = calc.generate_timeseries_json(birthdate)
        
        return jsonify({
            'status': 'success',
            'data': data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# Usage: GET /biorhythm?birthdate=1990-05-15&days=30
```

## 5. Configuration Options

### Chart Customization

```python
# Different chart sizes and orientations
configs = [
    BiorhythmCalculator(width=40, days=14, orientation="vertical"),    # Compact
    BiorhythmCalculator(width=80, days=60, orientation="horizontal"),  # Wide timeline
    BiorhythmCalculator(width=55, days=30, orientation="vertical")     # Default
]

birthdate = datetime(1990, 5, 15)
for i, calc in enumerate(configs):
    print(f"\n=== Configuration {i+1} ===")
    if i < 2:  # Show charts for first 2 configs only
        calc.generate_chart(birthdate)
    
    # Always show data summary
    data = calc.generate_timeseries_json(birthdate)
    print(f"Generated {len(data['timeseries'])} data points")
```

### Performance Considerations

```python
import time

# Benchmark different data sizes
sizes = [30, 90, 365, 1000]
birthdate = datetime(1990, 5, 15)

print("Performance Benchmarks:")
for days in sizes:
    calc = BiorhythmCalculator(days=days)
    
    start_time = time.time()
    data = calc.generate_timeseries_json(birthdate)
    elapsed = time.time() - start_time
    
    data_size = len(str(data))
    print(f"  {days:4d} days: {elapsed:.3f}s, {data_size:,} bytes")
```

## Next Steps

### 📚 **Learn More:**
- **[Complete API Reference](api/calculator.md)** - All methods and parameters
- **[JSON Data Format](api/json-schema.md)** - Detailed data structure
- **[Integration Examples](guides/integration.md)** - Advanced usage patterns

### 📊 **For Data Analysis:**
- **[Time Series Examples](../examples/time-series/)** - Pandas workflows
- **[Visualization Gallery](../examples/notebooks/)** - Chart examples
- **[Statistical Analysis](../examples/time-series/statistical-analysis.md)** - Correlation studies

### 🛠 **For Developers:**
- **[Advanced Usage](guides/advanced-usage.md)** - Configuration and optimization
- **[Error Handling](api/errors.md)** - Exception handling
- **[Performance Guide](reference/performance.md)** - Scaling and optimization

## Common Issues

### ImportError
```python
# If you get: ImportError: No module named 'biorythm'
# Make sure the package is installed:
import sys
print(sys.path)  # Check if package location is in path

# Reinstall if needed:
# pip uninstall biorythm
# pip install biorythm
```

### Date Format Issues
```python
from datetime import datetime

# Correct date formats
birthdate = datetime(1990, 5, 15)              # Year, month, day
birthdate = datetime.strptime('1990-05-15', '%Y-%m-%d')  # From string

# Avoid common mistakes
# birthdate = datetime(15, 5, 1990)  # Wrong order
# birthdate = datetime('1990-05-15')  # Wrong type
```

### Memory with Large Datasets
```python
# For very large datasets (>5000 days), process in chunks
def process_large_dataset(birthdate, total_days, chunk_size=1000):
    """Process large biorhythm datasets in chunks."""
    results = []
    
    for i in range(0, total_days, chunk_size):
        days_remaining = min(chunk_size, total_days - i)
        start_date = birthdate + timedelta(days=i)
        
        calc = BiorhythmCalculator(days=days_remaining)
        chunk_data = calc.generate_timeseries_json(birthdate, start_date)
        results.extend(chunk_data['timeseries'])
        
        print(f"Processed {i + days_remaining}/{total_days} days")
    
    return results
```

---

**🎯 You're now ready to integrate PyBiorythm into your Python projects!** 

This quickstart covered the essentials for package usage. Explore the links above for advanced features, data analysis workflows, and integration patterns.