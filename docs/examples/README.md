# Data Analysis Examples

Welcome to the PyBiorythm data analysis examples! This section is designed for **data scientists, researchers, and analysts** who want to use biorhythm data in their analytical workflows.

!!! info "Target Audience"
    This section focuses on **data analysis workflows** using biorhythm data. If you're looking for basic package usage, see the [Package Documentation](../package/).

## What You'll Find Here

### 📊 **Time Series Analysis**
Learn how to analyze biorhythm patterns using pandas, statistical methods, and time series techniques.

- **[Basic Analysis](time-series/basic-analysis.md)** - Getting started with pandas and descriptive statistics
- **[Visualization](time-series/visualization.md)** - Creating charts with matplotlib, plotly, and seaborn  
- **[Statistical Analysis](time-series/statistical-analysis.md)** - Correlation studies, trend detection, and hypothesis testing
- **[Machine Learning](time-series/machine-learning.md)** - Feature engineering and predictive modeling

### 📁 **Data Formats**
Understand biorhythm data structures and convert between formats for different analysis tools.

- **[JSON Timeseries](data-formats/json-timeseries.md)** - Deep dive into the biorhythm JSON structure
- **[CSV Export](data-formats/csv-export.md)** - Converting to CSV for Excel, R, and other tools
- **[Database Integration](data-formats/database-integration.md)** - Storing and querying biorhythm data

### 📓 **Interactive Notebooks**  
Ready-to-run Jupyter notebooks with complete analysis workflows.

- **[Biorhythm Analysis](notebooks/biorhythm-analysis.ipynb)** - Comprehensive analysis walkthrough
- **[Correlation Study](notebooks/correlation-study.ipynb)** - Statistical correlation analysis
- **[Visualization Gallery](notebooks/visualization-gallery.ipynb)** - Chart examples with multiple libraries

### 📈 **Sample Datasets**
Pre-generated datasets for experimentation and learning.

- **[Sample Data](datasets/)** - Various biorhythm datasets ready for analysis
- **[Data Dictionary](datasets/data-dictionary.md)** - Field descriptions and metadata

## Quick Start for Analysts

### 1. Generate Analysis-Ready Data

```python
import pandas as pd
from datetime import datetime
from biorythm import BiorhythmCalculator

# Generate 1 year of biorhythm data
calc = BiorhythmCalculator(days=365)
data = calc.generate_timeseries_json(datetime(1990, 5, 15))

# Convert to pandas DataFrame
df = pd.json_normalize(data['timeseries'])
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Rename columns for easier analysis
df.columns = ['day_number', 'physical', 'emotional', 'intellectual', 'critical_days']

print("Dataset ready for analysis:")
print(f"  Shape: {df.shape}")
print(f"  Date range: {df.index.min()} to {df.index.max()}")
print(f"  Columns: {list(df.columns)}")
```

### 2. Basic Statistical Analysis

```python
# Descriptive statistics
print("Biorhythm Cycle Statistics:")
cycle_stats = df[['physical', 'emotional', 'intellectual']].describe()
print(cycle_stats)

# Correlation analysis  
correlations = df[['physical', 'emotional', 'intellectual']].corr()
print("\nCycle Correlations:")
print(correlations)

# Find critical days (cycle transitions)
critical_days = df[df['critical_days'].str.len() > 0]
print(f"\nCritical days found: {len(critical_days)} out of {len(df)} ({len(critical_days)/len(df)*100:.1f}%)")
```

### 3. Visualization

```python
import matplotlib.pyplot as plt

# Plot all cycles
fig, ax = plt.subplots(figsize=(14, 8))

ax.plot(df.index, df['physical'], label='Physical (23d)', linewidth=2, alpha=0.8)
ax.plot(df.index, df['emotional'], label='Emotional (28d)', linewidth=2, alpha=0.8)  
ax.plot(df.index, df['intellectual'], label='Intellectual (33d)', linewidth=2, alpha=0.8)

# Mark critical days
if not critical_days.empty:
    ax.scatter(critical_days.index, [0] * len(critical_days), 
              color='red', s=30, alpha=0.7, zorder=5, label='Critical Days')

ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
ax.set_ylabel('Cycle Value')
ax.set_title('Biorhythm Cycles - One Year Analysis')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()
```

## Analysis Use Cases

### 🔍 **Research Applications**
- **Chronobiology studies** - Analyze biological rhythm patterns  
- **Performance research** - Correlate cycles with productivity metrics
- **Health studies** - Examine patterns in health or wellness data
- **Behavioral analysis** - Study decision-making patterns over time

### 📊 **Business Analytics**
- **Workforce planning** - Understand team performance patterns
- **Customer behavior** - Analyze purchasing or engagement cycles
- **Market research** - Study cyclical trends in business data  
- **Resource optimization** - Plan activities based on predicted patterns

### 🧪 **Educational Projects**
- **Statistics coursework** - Time series analysis practice
- **Data science portfolios** - Demonstrating analytical skills
- **Research methodology** - Learning correlation and trend analysis
- **Visualization practice** - Creating compelling data stories

## Data Science Workflow Examples

### Typical Analysis Pipeline

```python
# 1. Data Generation
def generate_biorhythm_dataset(birthdate, years=1):
    """Generate a biorhythm dataset for analysis."""
    days = years * 365
    calc = BiorhythmCalculator(days=days)
    data = calc.generate_timeseries_json(birthdate)
    
    df = pd.json_normalize(data['timeseries'])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    return df

# 2. Data Preprocessing  
def preprocess_biorhythm_data(df):
    """Clean and prepare biorhythm data for analysis."""
    # Rename columns
    df.rename(columns={
        'cycles.physical': 'physical',
        'cycles.emotional': 'emotional',
        'cycles.intellectual': 'intellectual'
    }, inplace=True)
    
    # Add derived features
    df['physical_emotional'] = df['physical'] * df['emotional']
    df['all_cycles_avg'] = df[['physical', 'emotional', 'intellectual']].mean(axis=1)
    df['cycle_variance'] = df[['physical', 'emotional', 'intellectual']].var(axis=1)
    
    # Add temporal features
    df['day_of_week'] = df.index.dayofweek
    df['day_of_month'] = df.index.day
    df['day_of_year'] = df.index.dayofyear
    df['week_of_year'] = df.index.isocalendar().week
    df['month'] = df.index.month
    
    return df

# 3. Statistical Analysis
def analyze_patterns(df):
    """Perform comprehensive pattern analysis."""
    results = {}
    
    # Basic statistics
    results['descriptive'] = df[['physical', 'emotional', 'intellectual']].describe()
    
    # Correlation analysis
    results['correlations'] = df[['physical', 'emotional', 'intellectual']].corr()
    
    # Seasonal patterns (by month)
    results['monthly_patterns'] = df.groupby('month')[['physical', 'emotional', 'intellectual']].mean()
    
    # Weekly patterns
    results['weekly_patterns'] = df.groupby('day_of_week')[['physical', 'emotional', 'intellectual']].mean()
    
    return results

# Example usage
birthdate = datetime(1985, 3, 22)
df = generate_biorhythm_dataset(birthdate, years=2)
df = preprocess_biorhythm_data(df) 
analysis = analyze_patterns(df)

print("Analysis complete. Results available in 'analysis' dictionary.")
```

### Advanced Analytics

```python
# Time series decomposition
from statsmodels.tsa.seasonal import seasonal_decompose

def decompose_biorhythm_cycles(df):
    """Perform time series decomposition on biorhythm cycles."""
    decompositions = {}
    
    for cycle in ['physical', 'emotional', 'intellectual']:
        # Perform seasonal decomposition
        decomp = seasonal_decompose(df[cycle], model='additive', period=30)
        
        decompositions[cycle] = {
            'trend': decomp.trend,
            'seasonal': decomp.seasonal, 
            'residual': decomp.resid,
            'original': df[cycle]
        }
    
    return decompositions

# Fourier analysis for frequency detection
import numpy as np
from scipy.fft import fft, fftfreq

def analyze_frequencies(df):
    """Analyze dominant frequencies in biorhythm data."""
    results = {}
    
    for cycle in ['physical', 'emotional', 'intellectual']:
        # Compute FFT
        data = df[cycle].values
        n = len(data)
        fft_vals = fft(data)
        freqs = fftfreq(n, d=1.0)  # Daily sampling
        
        # Find dominant frequencies (exclude DC component)
        power = np.abs(fft_vals[1:n//2])
        dominant_freq_idx = np.argmax(power) + 1
        dominant_period = 1.0 / freqs[dominant_freq_idx]
        
        results[cycle] = {
            'dominant_period_days': dominant_period,
            'theoretical_period': 23 if cycle=='physical' else 28 if cycle=='emotional' else 33,
            'frequency_accuracy': abs(dominant_period - (23 if cycle=='physical' else 28 if cycle=='emotional' else 33))
        }
    
    return results

# Example advanced analysis
decomp_results = decompose_biorhythm_cycles(df)
freq_results = analyze_frequencies(df)

print("Advanced analysis complete:")
print("- Time series decomposition available")  
print("- Frequency analysis shows period accuracy")
```

## Getting Help

### 📚 **Documentation References**
- **[Package API](../package/api/)** - Complete method reference
- **[Integration Guide](../package/guides/integration.md)** - Library integration patterns
- **[JSON Schema](../package/api/json-schema.md)** - Data format specifications

### 🛠 **Tools and Libraries**
This section assumes familiarity with:
- **pandas** - Data manipulation and analysis
- **matplotlib/plotly/seaborn** - Data visualization  
- **numpy/scipy** - Numerical computing and statistics
- **scikit-learn** - Machine learning (where applicable)
- **Jupyter** - Interactive notebook environment

### 💡 **Tips for Analysts**
1. **Start with sample data** - Use provided datasets to learn the structure
2. **Focus on correlations** - Biorhythm cycles have interesting statistical properties
3. **Visualize first** - Charts help understand patterns before statistical analysis
4. **Consider seasonality** - Look for patterns at different time scales
5. **Validate assumptions** - Test whether biorhythm theory holds in your data

---

**Ready to dive in?** Start with [Basic Analysis](time-series/basic-analysis.md) or jump straight to the [Jupyter Notebooks](notebooks/) for hands-on examples!