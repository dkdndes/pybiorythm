# Basic Time Series Analysis

This guide shows how to perform fundamental time series analysis on biorhythm data using pandas and basic statistical methods. Perfect for analysts getting started with biorhythm data exploration.

## Setup and Data Loading

### Prerequisites

```bash
pip install pandas matplotlib seaborn scipy statsmodels
```

### Generate Analysis Dataset

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from biorythm import BiorhythmCalculator

# Set up analysis parameters
BIRTHDATE = datetime(1990, 5, 15)  # Example person
ANALYSIS_PERIOD_DAYS = 365         # One year of data
START_DATE = datetime(2024, 1, 1)  # Analysis start

def create_analysis_dataset(birthdate, start_date=None, days=365):
    """Create a comprehensive biorhythm dataset for analysis."""
    
    calc = BiorhythmCalculator(days=days)
    raw_data = calc.generate_timeseries_json(birthdate, start_date)
    
    # Convert to DataFrame
    df = pd.json_normalize(raw_data['timeseries'])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    # Rename columns for easier analysis
    df.rename(columns={
        'cycles.physical': 'physical',
        'cycles.emotional': 'emotional',
        'cycles.intellectual': 'intellectual'
    }, inplace=True)
    
    # Add metadata as attributes
    df.attrs['metadata'] = raw_data['metadata']
    df.attrs['birthdate'] = birthdate
    df.attrs['analysis_period'] = days
    
    return df

# Create our analysis dataset
df = create_analysis_dataset(BIRTHDATE, START_DATE, ANALYSIS_PERIOD_DAYS)

print("Dataset created:")
print(f"  Shape: {df.shape}")
print(f"  Date range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
print(f"  Columns: {list(df.columns)}")
print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
```

## Descriptive Statistics

### Basic Statistical Summary

```python
# Comprehensive statistical overview
def analyze_descriptive_statistics(df):
    """Generate comprehensive descriptive statistics."""
    
    cycle_columns = ['physical', 'emotional', 'intellectual']
    stats_results = {}
    
    # Basic descriptive statistics
    basic_stats = df[cycle_columns].describe()
    stats_results['descriptive'] = basic_stats
    
    # Additional statistical measures
    additional_stats = pd.DataFrame(index=cycle_columns)
    additional_stats['skewness'] = df[cycle_columns].skew()
    additional_stats['kurtosis'] = df[cycle_columns].kurtosis()
    additional_stats['range'] = df[cycle_columns].max() - df[cycle_columns].min()
    additional_stats['iqr'] = df[cycle_columns].quantile(0.75) - df[cycle_columns].quantile(0.25)
    
    stats_results['additional'] = additional_stats
    
    # Correlation matrix
    correlation_matrix = df[cycle_columns].corr()
    stats_results['correlations'] = correlation_matrix
    
    return stats_results

# Perform analysis
stats = analyze_descriptive_statistics(df)

print("=== BIORHYTHM DESCRIPTIVE STATISTICS ===")
print("\n1. Basic Statistics:")
print(stats['descriptive'].round(3))

print("\n2. Additional Measures:")
print(stats['additional'].round(3))

print("\n3. Cycle Correlations:")
print(stats['correlations'].round(3))

# Interpretation guide
print("\n=== INTERPRETATION GUIDE ===")
print("• Mean should be ~0 (cycles are centered)")
print("• Std should be ~0.707 (RMS of sine wave)")  
print("• Min/Max should be close to -1/+1")
print("• Skewness ~0 indicates symmetry")
print("• Kurtosis ~-1.2 is expected for sine waves")
```

### Statistical Validation

```python
from scipy import stats

def validate_biorhythm_properties(df):
    """Validate expected mathematical properties of biorhythm cycles."""
    
    validation_results = {}
    cycle_columns = ['physical', 'emotional', 'intellectual']
    expected_periods = [23, 28, 33]
    
    for i, cycle in enumerate(cycle_columns):
        cycle_data = df[cycle].values
        results = {}
        
        # Test 1: Range validation (-1 to +1)
        results['min_value'] = cycle_data.min()
        results['max_value'] = cycle_data.max()
        results['range_valid'] = (-1.1 <= cycle_data.min() <= -0.9) and (0.9 <= cycle_data.max() <= 1.1)
        
        # Test 2: Mean should be close to zero
        results['mean'] = cycle_data.mean()
        results['mean_valid'] = abs(cycle_data.mean()) < 0.05
        
        # Test 3: Standard deviation should be ~0.707 (RMS of sine wave)
        results['std'] = cycle_data.std()
        results['std_valid'] = 0.6 < cycle_data.std() < 0.8
        
        # Test 4: Normality test (should fail - sine waves aren't normal)
        _, p_normal = stats.normaltest(cycle_data)
        results['normality_p'] = p_normal
        results['non_normal'] = p_normal < 0.05  # Should be True
        
        # Test 5: Periodicity check using autocorrelation
        expected_period = expected_periods[i]
        if len(cycle_data) > expected_period * 2:  # Need enough data
            autocorr = pd.Series(cycle_data).autocorr(lag=expected_period)
            results['period_autocorr'] = autocorr
            results['periodic'] = autocorr > 0.8  # Should be high for periodic data
        
        validation_results[cycle] = results
    
    return validation_results

# Validate biorhythm properties
validation = validate_biorhythm_properties(df)

print("=== BIORHYTHM VALIDATION RESULTS ===")
for cycle, results in validation.items():
    print(f"\n{cycle.upper()} CYCLE:")
    print(f"  Range: {results['min_value']:.3f} to {results['max_value']:.3f} ({'✓' if results['range_valid'] else '✗'})")
    print(f"  Mean: {results['mean']:.4f} ({'✓' if results['mean_valid'] else '✗'})")
    print(f"  Std: {results['std']:.3f} ({'✓' if results['std_valid'] else '✗'})")
    print(f"  Non-normal: {'✓' if results['non_normal'] else '✗'} (p={results['normality_p']:.4f})")
    if 'period_autocorr' in results:
        print(f"  Periodic: {'✓' if results['periodic'] else '✗'} (r={results['period_autocorr']:.3f})")
```

## Time Series Patterns

### Trend Analysis

```python
def analyze_trends(df, window_size=30):
    """Analyze trends in biorhythm cycles using moving averages."""
    
    cycle_columns = ['physical', 'emotional', 'intellectual']
    trend_results = {}
    
    for cycle in cycle_columns:
        # Calculate moving averages of different windows
        df[f'{cycle}_ma7'] = df[cycle].rolling(window=7).mean()
        df[f'{cycle}_ma{window_size}'] = df[cycle].rolling(window=window_size).mean()
        df[f'{cycle}_ma90'] = df[cycle].rolling(window=90).mean()
        
        # Calculate trend strength (slope of long-term moving average)
        ma_values = df[f'{cycle}_ma{window_size}'].dropna()
        if len(ma_values) > 30:
            x = np.arange(len(ma_values))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, ma_values)
            
            trend_results[cycle] = {
                'slope': slope,
                'r_squared': r_value**2,
                'p_value': p_value,
                'trend_strength': 'Strong' if abs(r_value) > 0.5 else 'Weak' if abs(r_value) > 0.2 else 'None'
            }
    
    return trend_results

# Analyze trends
trends = analyze_trends(df)

print("=== TREND ANALYSIS ===")
for cycle, result in trends.items():
    print(f"\n{cycle.upper()}:")
    print(f"  Trend slope: {result['slope']:.6f}")
    print(f"  R²: {result['r_squared']:.3f}")
    print(f"  Significance: p={result['p_value']:.4f}")
    print(f"  Trend strength: {result['trend_strength']}")

# Visualize trends
fig, axes = plt.subplots(3, 1, figsize=(14, 12))
cycle_columns = ['physical', 'emotional', 'intellectual']
colors = ['red', 'blue', 'green']

for i, (cycle, color) in enumerate(zip(cycle_columns, colors)):
    ax = axes[i]
    
    # Original data
    ax.plot(df.index, df[cycle], alpha=0.3, color=color, label='Daily values')
    
    # Moving averages
    ax.plot(df.index, df[f'{cycle}_ma7'], alpha=0.7, color=color, linewidth=1, label='7-day MA')
    ax.plot(df.index, df[f'{cycle}_ma30'], color=color, linewidth=2, label='30-day MA')
    ax.plot(df.index, df[f'{cycle}_ma90'], color='black', linewidth=2, linestyle='--', label='90-day MA')
    
    ax.set_title(f'{cycle.title()} Cycle - Trend Analysis')
    ax.set_ylabel('Cycle Value')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.2)

plt.tight_layout()
plt.show()
```

### Seasonal Patterns

```python
def analyze_seasonal_patterns(df):
    """Analyze seasonal and cyclical patterns in biorhythm data."""
    
    # Add temporal features for seasonal analysis
    df_seasonal = df.copy()
    df_seasonal['day_of_week'] = df_seasonal.index.dayofweek
    df_seasonal['day_of_month'] = df_seasonal.index.day
    df_seasonal['month'] = df_seasonal.index.month
    df_seasonal['day_of_year'] = df_seasonal.index.dayofyear
    df_seasonal['week_of_year'] = df_seasonal.index.isocalendar().week
    
    seasonal_results = {}
    cycle_columns = ['physical', 'emotional', 'intellectual']
    
    # Monthly patterns
    monthly_patterns = df_seasonal.groupby('month')[cycle_columns].agg(['mean', 'std'])
    seasonal_results['monthly'] = monthly_patterns
    
    # Day of week patterns  
    weekly_patterns = df_seasonal.groupby('day_of_week')[cycle_columns].agg(['mean', 'std'])
    seasonal_results['weekly'] = weekly_patterns
    
    # Day of month patterns (potential lunar cycle influence)
    daily_patterns = df_seasonal.groupby('day_of_month')[cycle_columns].mean()
    seasonal_results['daily'] = daily_patterns
    
    return seasonal_results, df_seasonal

# Analyze seasonal patterns
seasonal, df_with_temporal = analyze_seasonal_patterns(df)

print("=== SEASONAL PATTERN ANALYSIS ===")

# Monthly patterns
print("\n1. Monthly Averages (by calendar month):")
monthly_means = seasonal['monthly'].xs('mean', level=1, axis=1)
print(monthly_means.round(3))

# Weekly patterns
print("\n2. Day of Week Patterns (0=Monday, 6=Sunday):")
weekly_means = seasonal['weekly'].xs('mean', level=1, axis=1)
print(weekly_means.round(3))

# Statistical significance of seasonal patterns
from scipy.stats import f_oneway

print("\n3. Statistical Significance of Seasonal Patterns:")
for cycle in ['physical', 'emotional', 'intellectual']:
    # Test monthly differences
    monthly_groups = [df_with_temporal[df_with_temporal['month'] == month][cycle].values 
                     for month in range(1, 13)]
    f_stat, p_value = f_oneway(*monthly_groups)
    
    print(f"  {cycle.title()} - Monthly variation: F={f_stat:.3f}, p={p_value:.4f}")
    
    # Test weekly differences  
    weekly_groups = [df_with_temporal[df_with_temporal['day_of_week'] == day][cycle].values
                    for day in range(7)]
    f_stat, p_value = f_oneway(*weekly_groups)
    
    print(f"  {cycle.title()} - Weekly variation: F={f_stat:.3f}, p={p_value:.4f}")
```

### Critical Day Analysis

```python
def analyze_critical_days(df):
    """Analyze patterns in critical days (cycle zero crossings)."""
    
    cycle_columns = ['physical', 'emotional', 'intellectual']
    critical_analysis = {}
    
    # Find critical days for each cycle (values close to zero)
    threshold = 0.05  # Consider values within 0.05 of zero as "critical"
    
    for cycle in cycle_columns:
        cycle_data = df[cycle]
        
        # Find critical days
        critical_mask = np.abs(cycle_data) < threshold
        critical_days = df[critical_mask]
        
        # Analyze critical day patterns
        if len(critical_days) > 0:
            # Frequency analysis
            total_days = len(df)
            critical_frequency = len(critical_days) / total_days
            
            # Expected frequency for sine wave (theoretical)
            # For sine wave, ~12.7% of values should be within 0.05 of zero
            expected_frequency = 2 * np.arcsin(threshold) / np.pi
            
            # Time between critical days
            critical_intervals = critical_days.index.to_series().diff().dt.days.dropna()
            
            critical_analysis[cycle] = {
                'total_critical_days': len(critical_days),
                'critical_frequency': critical_frequency,
                'expected_frequency': expected_frequency,
                'frequency_ratio': critical_frequency / expected_frequency,
                'mean_interval': critical_intervals.mean() if len(critical_intervals) > 0 else None,
                'std_interval': critical_intervals.std() if len(critical_intervals) > 0 else None,
                'critical_dates': critical_days.index.tolist()
            }
    
    return critical_analysis

# Analyze critical days
critical_results = analyze_critical_days(df)

print("=== CRITICAL DAY ANALYSIS ===")
for cycle, results in critical_results.items():
    print(f"\n{cycle.upper()} CYCLE:")
    print(f"  Critical days found: {results['total_critical_days']}")
    print(f"  Frequency: {results['critical_frequency']:.3f} ({results['critical_frequency']*100:.1f}%)")
    print(f"  Expected frequency: {results['expected_frequency']:.3f} ({results['expected_frequency']*100:.1f}%)")
    print(f"  Frequency ratio: {results['frequency_ratio']:.2f}")
    if results['mean_interval']:
        print(f"  Mean interval: {results['mean_interval']:.1f} ± {results['std_interval']:.1f} days")

# Visualize critical days
fig, ax = plt.subplots(figsize=(14, 8))

# Plot cycles
for cycle, color in zip(['physical', 'emotional', 'intellectual'], ['red', 'blue', 'green']):
    ax.plot(df.index, df[cycle], label=f'{cycle.title()}', color=color, alpha=0.7)
    
    # Mark critical days
    critical_dates = critical_results[cycle]['critical_dates']
    if critical_dates:
        critical_values = [df.loc[date, cycle] for date in critical_dates]
        ax.scatter(critical_dates, critical_values, color=color, s=30, alpha=0.8, 
                  marker='o', edgecolor='black', linewidth=0.5)

ax.axhline(y=0, color='black', linestyle='-', alpha=0.3, linewidth=2)
ax.axhline(y=0.05, color='gray', linestyle='--', alpha=0.5, label='Critical threshold')
ax.axhline(y=-0.05, color='gray', linestyle='--', alpha=0.5)

ax.set_title('Biorhythm Cycles with Critical Days Marked')
ax.set_ylabel('Cycle Value')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()
```

## Data Quality Assessment

### Missing Data and Anomalies

```python
def assess_data_quality(df):
    """Assess data quality and identify potential anomalies."""
    
    quality_report = {}
    cycle_columns = ['physical', 'emotional', 'intellectual']
    
    # Check for missing values
    missing_data = df[cycle_columns].isnull().sum()
    quality_report['missing_values'] = missing_data
    
    # Check for duplicate dates
    duplicate_dates = df.index.duplicated().sum()
    quality_report['duplicate_dates'] = duplicate_dates
    
    # Check for values outside expected range
    range_violations = {}
    for cycle in cycle_columns:
        out_of_range = ((df[cycle] < -1.1) | (df[cycle] > 1.1)).sum()
        range_violations[cycle] = out_of_range
    quality_report['range_violations'] = range_violations
    
    # Detect potential outliers using IQR method
    outliers = {}
    for cycle in cycle_columns:
        Q1 = df[cycle].quantile(0.25)
        Q3 = df[cycle].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outlier_mask = (df[cycle] < lower_bound) | (df[cycle] > upper_bound)
        outliers[cycle] = df[outlier_mask][cycle]
    
    quality_report['outliers'] = outliers
    
    # Check data continuity (gaps in dates)
    expected_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    missing_dates = expected_dates.difference(df.index)
    quality_report['missing_dates'] = missing_dates.tolist()
    
    return quality_report

# Assess data quality
quality = assess_data_quality(df)

print("=== DATA QUALITY ASSESSMENT ===")

print(f"\n1. Missing Values:")
for cycle, count in quality['missing_values'].items():
    print(f"   {cycle}: {count}")

print(f"\n2. Duplicate Dates: {quality['duplicate_dates']}")

print(f"\n3. Range Violations (|value| > 1.1):")
for cycle, count in quality['range_violations'].items():
    print(f"   {cycle}: {count}")

print(f"\n4. Statistical Outliers (IQR method):")
for cycle, outliers in quality['outliers'].items():
    print(f"   {cycle}: {len(outliers)} outliers")
    if len(outliers) > 0:
        print(f"      Range: {outliers.min():.3f} to {outliers.max():.3f}")

print(f"\n5. Missing Dates: {len(quality['missing_dates'])}")
if len(quality['missing_dates']) > 0:
    print(f"   First few: {quality['missing_dates'][:5]}")

# Overall data quality score
total_issues = (quality['missing_values'].sum() + 
                quality['duplicate_dates'] + 
                sum(quality['range_violations'].values()) + 
                len(quality['missing_dates']))

data_quality_score = max(0, 100 - (total_issues / len(df) * 100))
print(f"\n=== OVERALL DATA QUALITY SCORE: {data_quality_score:.1f}/100 ===")
```

## Summary and Export

```python
def generate_analysis_summary(df, stats, trends, seasonal, critical_results, quality):
    """Generate a comprehensive analysis summary."""
    
    summary = {
        'dataset_info': {
            'total_days': len(df),
            'date_range': f"{df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}",
            'birthdate': df.attrs.get('birthdate', 'Unknown'),
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'key_findings': {},
        'recommendations': []
    }
    
    # Key statistical findings
    cycle_columns = ['physical', 'emotional', 'intellectual']
    for cycle in cycle_columns:
        findings = {
            'mean': stats['descriptive'].loc['mean', cycle],
            'std': stats['descriptive'].loc['std', cycle],
            'range': stats['descriptive'].loc['max', cycle] - stats['descriptive'].loc['min', cycle],
            'critical_days': critical_results[cycle]['total_critical_days'],
            'trend_strength': trends[cycle]['trend_strength']
        }
        summary['key_findings'][cycle] = findings
    
    # Generate recommendations
    if data_quality_score > 95:
        summary['recommendations'].append("Data quality is excellent - suitable for all analysis types")
    elif data_quality_score > 80:
        summary['recommendations'].append("Data quality is good - suitable for most analyses")
    else:
        summary['recommendations'].append("Data quality issues detected - review before detailed analysis")
    
    # Correlation insights
    max_correlation = stats['correlations'].abs().max().max()
    if max_correlation > 0.5:
        summary['recommendations'].append("Strong correlations detected between cycles - investigate further")
    
    return summary

# Generate final summary
summary = generate_analysis_summary(df, stats, trends, seasonal, critical_results, quality)

print("=== ANALYSIS SUMMARY ===")
print(f"\nDataset: {summary['dataset_info']['total_days']} days ({summary['dataset_info']['date_range']})")
print(f"Analysis completed: {summary['dataset_info']['analysis_date']}")

print(f"\nKey Findings:")
for cycle, findings in summary['key_findings'].items():
    print(f"  {cycle.title()}:")
    print(f"    Mean: {findings['mean']:.3f}, Std: {findings['std']:.3f}")
    print(f"    Critical days: {findings['critical_days']}, Trend: {findings['trend_strength']}")

print(f"\nRecommendations:")
for rec in summary['recommendations']:
    print(f"  • {rec}")

# Export results for further analysis
export_data = {
    'timeseries': df.to_dict('records'),
    'statistics': stats['descriptive'].to_dict(),
    'correlations': stats['correlations'].to_dict(),
    'summary': summary
}

# Save to JSON for use in other tools
import json
with open('biorhythm_analysis_results.json', 'w') as f:
    json.dump(export_data, f, indent=2, default=str)

print(f"\n=== Results exported to 'biorhythm_analysis_results.json' ===")
```

## Next Steps

This basic analysis provides a foundation for understanding biorhythm time series data. Continue with:

- **[Visualization](visualization.md)** - Create compelling charts and plots
- **[Statistical Analysis](statistical-analysis.md)** - Advanced statistical methods  
- **[Machine Learning](machine-learning.md)** - Predictive modeling and pattern recognition
- **[Jupyter Notebooks](../notebooks/)** - Interactive analysis environments

The exported JSON file can be imported into other analysis tools or used as input for advanced modeling techniques.