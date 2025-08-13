# Integration Guide

This guide shows how to integrate PyBiorythm with popular Python libraries for data analysis, visualization, web development, and scientific computing.

## Data Science Stack

### Pandas Integration

Transform biorhythm data into pandas DataFrames for powerful analysis:

```python
import pandas as pd
from datetime import datetime, timedelta
from biorythm import BiorhythmCalculator

def biorhythm_to_dataframe(birthdate, start_date=None, days=90):
    """Convert biorhythm data to pandas DataFrame."""
    calc = BiorhythmCalculator(days=days)
    data = calc.generate_timeseries_json(birthdate, start_date)
    
    # Convert to DataFrame
    df = pd.json_normalize(data['timeseries'])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    # Simplify column names
    df.rename(columns={
        'cycles.physical': 'physical',
        'cycles.emotional': 'emotional', 
        'cycles.intellectual': 'intellectual'
    }, inplace=True)
    
    return df

# Example usage
birthdate = datetime(1990, 5, 15)
df = biorhythm_to_dataframe(birthdate, days=365)

# Time series analysis
print("Annual Biorhythm Statistics:")
print(df[['physical', 'emotional', 'intellectual']].describe())

# Find correlations
correlations = df[['physical', 'emotional', 'intellectual']].corr()
print("\nCycle Correlations:")
print(correlations)

# Resample to weekly averages
weekly_avg = df.resample('W').mean()
print(f"\nWeekly averages calculated: {len(weekly_avg)} weeks")
```

### NumPy Integration

Use NumPy for high-performance calculations:

```python
import numpy as np
from biorythm import BiorhythmCalculator

def calculate_biorhythms_vectorized(birthdate, start_date, num_days):
    """High-performance biorhythm calculation using NumPy."""
    # Calculate base day number
    base_day = (start_date - birthdate).days
    
    # Create array of consecutive day numbers
    day_numbers = np.arange(base_day, base_day + num_days)
    
    # Vectorized calculation for all cycles
    cycles = {
        'physical': np.sin(2 * np.pi * day_numbers / 23),
        'emotional': np.sin(2 * np.pi * day_numbers / 28), 
        'intellectual': np.sin(2 * np.pi * day_numbers / 33)
    }
    
    # Create date array
    dates = np.array([start_date + timedelta(days=i) for i in range(num_days)])
    
    return dates, cycles

# Benchmark performance
import time

birthdate = datetime(1990, 5, 15)
start_date = datetime(2024, 1, 1)

# Standard method
start_time = time.time()
calc = BiorhythmCalculator(days=10000)
data = calc.generate_timeseries_json(birthdate, start_date)
standard_time = time.time() - start_time

# NumPy method
start_time = time.time()
dates, cycles = calculate_biorhythms_vectorized(birthdate, start_date, 10000)
numpy_time = time.time() - start_time

print(f"Standard method: {standard_time:.3f}s")
print(f"NumPy method: {numpy_time:.3f}s")
print(f"Speedup: {standard_time/numpy_time:.1f}x")
```

### SciPy Integration

Advanced statistical analysis with SciPy:

```python
from scipy import stats, signal
import numpy as np
import matplotlib.pyplot as plt

def analyze_biorhythm_patterns(df):
    """Statistical analysis of biorhythm patterns using SciPy."""
    
    results = {}
    cycles = ['physical', 'emotional', 'intellectual']
    
    for cycle in cycles:
        data = df[cycle].values
        
        # Basic statistics
        results[cycle] = {
            'mean': np.mean(data),
            'std': np.std(data),
            'skewness': stats.skew(data),
            'kurtosis': stats.kurtosis(data)
        }
        
        # Frequency analysis
        freqs, power = signal.periodogram(data, fs=1.0)  # 1 sample per day
        dominant_freq_idx = np.argmax(power[1:]) + 1  # Skip DC component
        dominant_period = 1.0 / freqs[dominant_freq_idx]
        results[cycle]['dominant_period_days'] = dominant_period
        
        # Statistical tests
        # Test for normality
        _, p_normal = stats.normaltest(data)
        results[cycle]['is_normal'] = p_normal > 0.05
        
        # Test for randomness (runs test)
        median = np.median(data)
        runs, runs_pvalue = stats.runs_test(data > median)
        results[cycle]['is_random'] = runs_pvalue > 0.05
    
    return results

# Example analysis
df = biorhythm_to_dataframe(datetime(1990, 5, 15), days=1000)
analysis = analyze_biorhythm_patterns(df)

for cycle, stats_dict in analysis.items():
    print(f"\n{cycle.upper()} CYCLE ANALYSIS:")
    for stat, value in stats_dict.items():
        if isinstance(value, bool):
            print(f"  {stat}: {value}")
        elif isinstance(value, float):
            print(f"  {stat}: {value:.3f}")
```

## Visualization Libraries

### Matplotlib Integration

Create publication-quality biorhythm visualizations:

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle

def create_biorhythm_chart(df, title="Biorhythm Cycles"):
    """Create a comprehensive biorhythm chart."""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Main cycles plot
    ax1.plot(df.index, df['physical'], label='Physical (23d)', 
             linewidth=2.5, color='#e74c3c', alpha=0.8)
    ax1.plot(df.index, df['emotional'], label='Emotional (28d)', 
             linewidth=2.5, color='#3498db', alpha=0.8)
    ax1.plot(df.index, df['intellectual'], label='Intellectual (33d)', 
             linewidth=2.5, color='#2ecc71', alpha=0.8)
    
    # Zero line
    ax1.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    
    # Highlight critical days
    critical_days = df[df['critical_days'].str.len() > 0]
    if not critical_days.empty:
        ax1.scatter(critical_days.index, [0] * len(critical_days), 
                   color='red', s=50, alpha=0.7, marker='o', 
                   label=f'Critical Days ({len(critical_days)})')
    
    # Formatting
    ax1.set_ylabel('Cycle Value', fontsize=12)
    ax1.set_title(title, fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-1.1, 1.1)
    
    # Format x-axis
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # Correlation heatmap
    corr_data = df[['physical', 'emotional', 'intellectual']].corr()
    im = ax2.imshow(corr_data, cmap='coolwarm', vmin=-1, vmax=1, aspect='equal')
    
    # Add correlation values
    for i in range(len(corr_data)):
        for j in range(len(corr_data)):
            text = ax2.text(j, i, f'{corr_data.iloc[i, j]:.2f}',
                           ha="center", va="center", color="black", fontweight='bold')
    
    ax2.set_xticks(range(len(corr_data.columns)))
    ax2.set_yticks(range(len(corr_data.columns)))
    ax2.set_xticklabels(corr_data.columns)
    ax2.set_yticklabels(corr_data.columns)
    ax2.set_title('Cycle Correlations', fontsize=12, fontweight='bold')
    
    plt.colorbar(im, ax=ax2, shrink=0.8)
    plt.tight_layout()
    return fig

# Create chart
df = biorhythm_to_dataframe(datetime(1990, 5, 15), days=90)
fig = create_biorhythm_chart(df, "3-Month Biorhythm Analysis")
plt.show()
```

### Plotly Integration

Interactive biorhythm visualizations:

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def create_interactive_biorhythm(df):
    """Create interactive biorhythm chart with Plotly."""
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Biorhythm Cycles Over Time', 'Cycle Distribution'),
        specs=[[{"secondary_y": False}], [{"type": "histogram"}]],
        row_heights=[0.7, 0.3]
    )
    
    # Main time series plot
    colors = {'physical': '#e74c3c', 'emotional': '#3498db', 'intellectual': '#2ecc71'}
    
    for cycle in ['physical', 'emotional', 'intellectual']:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[cycle], 
                mode='lines',
                name=f'{cycle.title()} ({23 if cycle=="physical" else 28 if cycle=="emotional" else 33}d)',
                line=dict(color=colors[cycle], width=3),
                hovertemplate=f'<b>{cycle.title()}</b><br>' +
                             'Date: %{x}<br>' +
                             'Value: %{y:.3f}<br>' +
                             '<extra></extra>'
            ),
            row=1, col=1
        )
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, row=1, col=1)
    
    # Add critical days
    critical_days = df[df['critical_days'].str.len() > 0]
    if not critical_days.empty:
        fig.add_trace(
            go.Scatter(
                x=critical_days.index,
                y=[0] * len(critical_days),
                mode='markers',
                name=f'Critical Days ({len(critical_days)})',
                marker=dict(color='red', size=8, symbol='diamond'),
                hovertemplate='<b>Critical Day</b><br>' +
                             'Date: %{x}<br>' +
                             '<extra></extra>'
            ),
            row=1, col=1
        )
    
    # Histogram of cycle values
    for cycle in ['physical', 'emotional', 'intellectual']:
        fig.add_trace(
            go.Histogram(
                x=df[cycle],
                name=f'{cycle.title()}',
                marker_color=colors[cycle],
                opacity=0.7,
                nbinsx=30
            ),
            row=2, col=1
        )
    
    # Update layout
    fig.update_layout(
        title="Interactive Biorhythm Analysis",
        height=800,
        hovermode='x unified'
    )
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="Cycle Value", range=[-1.1, 1.1], row=1, col=1)
    fig.update_xaxes(title_text="Cycle Value", row=2, col=1)
    fig.update_yaxes(title_text="Frequency", row=2, col=1)
    
    return fig

# Create interactive chart
df = biorhythm_to_dataframe(datetime(1990, 5, 15), days=90)
fig = create_interactive_biorhythm(df)
fig.show()
```

### Seaborn Integration

Statistical visualizations with Seaborn:

```python
import seaborn as sns
import matplotlib.pyplot as plt

def create_biorhythm_analysis_plots(df):
    """Create comprehensive statistical plots with Seaborn."""
    
    # Reshape data for Seaborn
    df_melted = df[['physical', 'emotional', 'intellectual']].reset_index().melt(
        id_vars='date', 
        var_name='cycle', 
        value_name='value'
    )
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Distribution plot
    sns.histplot(data=df_melted, x='value', hue='cycle', 
                 multiple='dodge', stat='density', 
                 ax=axes[0, 0])
    axes[0, 0].set_title('Cycle Value Distributions')
    axes[0, 0].set_xlabel('Cycle Value')
    
    # 2. Box plot by cycle
    sns.boxplot(data=df_melted, x='cycle', y='value', ax=axes[0, 1])
    axes[0, 1].set_title('Cycle Value Ranges')
    axes[0, 1].set_ylabel('Cycle Value')
    
    # 3. Correlation heatmap
    corr = df[['physical', 'emotional', 'intellectual']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0,
                square=True, ax=axes[1, 0])
    axes[1, 0].set_title('Cycle Correlations')
    
    # 4. Rolling correlation
    window = 30
    rolling_corr = df['physical'].rolling(window).corr(df['emotional'])
    
    axes[1, 1].plot(df.index, rolling_corr, label=f'Physical-Emotional ({window}d window)')
    axes[1, 1].set_title('Rolling Correlations')
    axes[1, 1].set_ylabel('Correlation')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# Create statistical plots
df = biorhythm_to_dataframe(datetime(1990, 5, 15), days=365)
fig = create_biorhythm_analysis_plots(df)
plt.show()
```

## Web Framework Integration

### Flask Integration

REST API for biorhythm calculations:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

@app.route('/api/biorhythm', methods=['POST'])
def calculate_biorhythm():
    """Calculate biorhythm data for given parameters."""
    try:
        data = request.get_json()
        
        # Parse parameters
        birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d')
        days = data.get('days', 30)
        start_date = data.get('start_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        
        # Generate biorhythm data
        calc = BiorhythmCalculator(days=days)
        result = calc.generate_timeseries_json(birthdate, start_date)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/biorhythm/current/<birthdate>')
def get_current_biorhythm(birthdate):
    """Get current biorhythm values for a birthdate."""
    try:
        birth_dt = datetime.strptime(birthdate, '%Y-%m-%d')
        calc = BiorhythmCalculator()
        
        physical, emotional, intellectual = calc.calculate_biorhythm_values(
            birth_dt, datetime.now()
        )
        
        return jsonify({
            'success': True,
            'data': {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'cycles': {
                    'physical': round(physical, 3),
                    'emotional': round(emotional, 3), 
                    'intellectual': round(intellectual, 3)
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI Integration

Modern async API with automatic documentation:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
import uvicorn

app = FastAPI(title="Biorhythm API", version="1.0.0")

class BiorhythmRequest(BaseModel):
    birthdate: date = Field(..., description="Birth date in YYYY-MM-DD format")
    days: int = Field(30, ge=1, le=1000, description="Number of days to calculate")
    start_date: Optional[date] = Field(None, description="Start date (default: today)")

class CycleValues(BaseModel):
    physical: float = Field(..., ge=-1, le=1)
    emotional: float = Field(..., ge=-1, le=1)
    intellectual: float = Field(..., ge=-1, le=1)

@app.post("/biorhythm", summary="Calculate biorhythm data")
async def calculate_biorhythm(request: BiorhythmRequest):
    """Calculate biorhythm data for the given parameters."""
    try:
        calc = BiorhythmCalculator(days=request.days)
        
        birthdate = datetime.combine(request.birthdate, datetime.min.time())
        start_date = None
        if request.start_date:
            start_date = datetime.combine(request.start_date, datetime.min.time())
        
        result = calc.generate_timeseries_json(birthdate, start_date)
        return {"success": True, "data": result}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/biorhythm/{birthdate}/current", response_model=dict)
async def get_current_biorhythm(birthdate: date):
    """Get current biorhythm values for a specific birth date."""
    try:
        calc = BiorhythmCalculator()
        birth_dt = datetime.combine(birthdate, datetime.min.time())
        
        physical, emotional, intellectual = calc.calculate_biorhythm_values(
            birth_dt, datetime.now()
        )
        
        return {
            "success": True,
            "data": {
                "date": datetime.now().date(),
                "cycles": CycleValues(
                    physical=physical,
                    emotional=emotional,
                    intellectual=intellectual
                ).dict()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run with: uvicorn integration_examples:app --reload
```

### Django Integration

Django model and views for biorhythm functionality:

```python
# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import json

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_current_biorhythm(self):
        """Get current biorhythm values for this user."""
        from biorythm import BiorhythmCalculator
        
        calc = BiorhythmCalculator()
        physical, emotional, intellectual = calc.calculate_biorhythm_values(
            datetime.combine(self.birthdate, datetime.min.time()),
            datetime.now()
        )
        
        return {
            'physical': round(physical, 3),
            'emotional': round(emotional, 3),
            'intellectual': round(intellectual, 3)
        }

class BiorhythmCache(models.Model):
    """Cache biorhythm calculations to improve performance."""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    start_date = models.DateField()
    days = models.IntegerField()
    data = models.TextField()  # JSON data
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user_profile', 'start_date', 'days']
    
    def get_data(self):
        return json.loads(self.data)
    
    def set_data(self, data_dict):
        self.data = json.dumps(data_dict)

# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

@login_required
@csrf_exempt
def user_biorhythm(request):
    """Get biorhythm data for authenticated user."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            days = data.get('days', 30)
            
            profile = get_object_or_404(UserProfile, user=request.user)
            
            # Check cache first
            cache_obj, created = BiorhythmCache.objects.get_or_create(
                user_profile=profile,
                start_date=datetime.now().date(),
                days=days,
                defaults={'data': '{}'}
            )
            
            if created or not cache_obj.data:
                # Calculate new data
                from biorythm import BiorhythmCalculator
                calc = BiorhythmCalculator(days=days)
                
                birthdate = datetime.combine(profile.birthdate, datetime.min.time())
                result = calc.generate_timeseries_json(birthdate)
                
                cache_obj.set_data(result)
                cache_obj.save()
            
            return JsonResponse({
                'success': True,
                'data': cache_obj.get_data()
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
```

## Machine Learning Integration

### Scikit-learn Feature Engineering

Use biorhythm data as features for ML models:

```python
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

def create_biorhythm_features(df, window_sizes=[7, 14, 30]):
    """Create ML features from biorhythm data."""
    
    feature_df = df.copy()
    cycles = ['physical', 'emotional', 'intellectual']
    
    # Rolling statistics
    for cycle in cycles:
        for window in window_sizes:
            feature_df[f'{cycle}_mean_{window}d'] = df[cycle].rolling(window).mean()
            feature_df[f'{cycle}_std_{window}d'] = df[cycle].rolling(window).std()
            feature_df[f'{cycle}_min_{window}d'] = df[cycle].rolling(window).min()
            feature_df[f'{cycle}_max_{window}d'] = df[cycle].rolling(window).max()
    
    # Cycle interactions
    feature_df['physical_emotional'] = df['physical'] * df['emotional']
    feature_df['physical_intellectual'] = df['physical'] * df['intellectual']
    feature_df['emotional_intellectual'] = df['emotional'] * df['intellectual']
    
    # Critical day indicators
    feature_df['physical_critical'] = np.abs(df['physical']) < 0.1
    feature_df['emotional_critical'] = np.abs(df['emotional']) < 0.1
    feature_df['intellectual_critical'] = np.abs(df['intellectual']) < 0.1
    feature_df['any_critical'] = (feature_df['physical_critical'] | 
                                  feature_df['emotional_critical'] | 
                                  feature_df['intellectual_critical'])
    
    # Temporal features
    feature_df['day_of_week'] = df.index.dayofweek
    feature_df['day_of_month'] = df.index.day
    feature_df['day_of_year'] = df.index.dayofyear
    
    return feature_df

# Example: Predict mood scores using biorhythm features
def predict_mood_with_biorhythm():
    """Example of using biorhythm data to predict synthetic mood scores."""
    
    # Generate biorhythm data
    df = biorhythm_to_dataframe(datetime(1990, 5, 15), days=365)
    
    # Create synthetic mood target (for demonstration)
    # In real use, this would be actual mood/performance data
    np.random.seed(42)
    df['mood_score'] = (
        0.3 * df['physical'] + 
        0.4 * df['emotional'] + 
        0.2 * df['intellectual'] + 
        0.1 * np.random.normal(0, 0.2, len(df))
    )
    
    # Create features
    feature_df = create_biorhythm_features(df)
    
    # Remove rows with NaN (from rolling windows)
    feature_df = feature_df.dropna()
    
    # Prepare data for ML
    feature_cols = [col for col in feature_df.columns 
                   if col not in ['mood_score'] and 
                      not col.startswith('critical_days')]
    
    X = feature_df[feature_cols]
    y = feature_df['mood_score']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    
    print(f"Model Performance:")
    print(f"  Mean Squared Error: {mse:.4f}")
    print(f"  R² Score: {model.score(X_test_scaled, y_test):.4f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Most Important Features:")
    print(feature_importance.head(10))
    
    return model, scaler, feature_cols

model, scaler, features = predict_mood_with_biorhythm()
```

## Database Integration

### SQLAlchemy Integration

Store and query biorhythm data efficiently:

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import json

Base = declarative_base()

class Person(Base):
    __tablename__ = 'persons'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    birthdate = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class BiorhythmData(Base):
    __tablename__ = 'biorhythm_data'
    
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, nullable=False)
    calculation_date = Column(Date, nullable=False)
    days_calculated = Column(Integer, nullable=False)
    data_json = Column(Text, nullable=False)  # JSON data
    created_at = Column(DateTime, default=datetime.utcnow)

def store_biorhythm_data(session, person_id, days=30):
    """Calculate and store biorhythm data for a person."""
    
    # Get person
    person = session.query(Person).filter_by(id=person_id).first()
    if not person:
        raise ValueError(f"Person with id {person_id} not found")
    
    # Calculate biorhythm
    calc = BiorhythmCalculator(days=days)
    birthdate = datetime.combine(person.birthdate, datetime.min.time())
    data = calc.generate_timeseries_json(birthdate)
    
    # Store in database
    biorhythm_record = BiorhythmData(
        person_id=person_id,
        calculation_date=date.today(),
        days_calculated=days,
        data_json=json.dumps(data)
    )
    
    session.add(biorhythm_record)
    session.commit()
    
    return biorhythm_record.id

# Example usage
engine = create_engine('sqlite:///biorhythm.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def demo_database_integration():
    session = Session()
    
    # Add a person
    person = Person(name="John Doe", birthdate=date(1990, 5, 15))
    session.add(person)
    session.commit()
    
    # Store biorhythm data
    record_id = store_biorhythm_data(session, person.id, days=90)
    print(f"Stored biorhythm data with record ID: {record_id}")
    
    # Query and analyze
    records = session.query(BiorhythmData).filter_by(person_id=person.id).all()
    for record in records:
        data = json.loads(record.data_json)
        print(f"Record {record.id}: {len(data['timeseries'])} days of data")
    
    session.close()

demo_database_integration()
```

## Testing Integration

### Pytest Integration

Test biorhythm calculations in your applications:

```python
import pytest
from datetime import datetime, timedelta
from biorythm import BiorhythmCalculator

class TestBiorhythmIntegration:
    """Test biorhythm integration with various scenarios."""
    
    @pytest.fixture
    def calculator(self):
        return BiorhythmCalculator(days=30)
    
    @pytest.fixture
    def sample_birthdate(self):
        return datetime(1990, 5, 15)
    
    def test_basic_calculation(self, calculator, sample_birthdate):
        """Test basic biorhythm calculation."""
        physical, emotional, intellectual = calculator.calculate_biorhythm_values(
            sample_birthdate, datetime(2024, 1, 15)
        )
        
        # Verify values are in expected range
        assert -1.0 <= physical <= 1.0
        assert -1.0 <= emotional <= 1.0
        assert -1.0 <= intellectual <= 1.0
    
    def test_json_output_structure(self, calculator, sample_birthdate):
        """Test JSON output has correct structure."""
        data = calculator.generate_timeseries_json(sample_birthdate)
        
        # Check top-level structure
        assert 'metadata' in data
        assert 'timeseries' in data
        
        # Check metadata
        metadata = data['metadata']
        assert 'birthdate' in metadata
        assert 'cycles' in metadata
        assert len(metadata['cycles']) == 3
        
        # Check timeseries
        timeseries = data['timeseries']
        assert len(timeseries) == 30  # Default days
        
        for entry in timeseries:
            assert 'date' in entry
            assert 'cycles' in entry
            assert len(entry['cycles']) == 3
    
    def test_pandas_integration(self, sample_birthdate):
        """Test integration with pandas DataFrame."""
        import pandas as pd
        
        calc = BiorhythmCalculator(days=90)
        data = calc.generate_timeseries_json(sample_birthdate)
        
        # Convert to DataFrame
        df = pd.json_normalize(data['timeseries'])
        df['date'] = pd.to_datetime(df['date'])
        
        # Verify DataFrame structure
        assert len(df) == 90
        assert 'cycles.physical' in df.columns
        assert 'cycles.emotional' in df.columns
        assert 'cycles.intellectual' in df.columns
        
        # Verify data types
        assert df['date'].dtype.name.startswith('datetime')
        assert df['cycles.physical'].dtype in ['float64', 'float32']
    
    @pytest.mark.parametrize("days", [1, 30, 90, 365])
    def test_different_periods(self, sample_birthdate, days):
        """Test calculation for different time periods."""
        calc = BiorhythmCalculator(days=days)
        data = calc.generate_timeseries_json(sample_birthdate)
        
        assert len(data['timeseries']) == days
        assert data['metadata']['chart_period_days'] == days
    
    def test_performance_benchmark(self, sample_birthdate):
        """Test performance for large datasets."""
        import time
        
        calc = BiorhythmCalculator(days=1000)
        
        start_time = time.time()
        data = calc.generate_timeseries_json(sample_birthdate)
        elapsed = time.time() - start_time
        
        # Should complete within reasonable time (adjust as needed)
        assert elapsed < 1.0  # 1 second max
        assert len(data['timeseries']) == 1000

if __name__ == '__main__':
    pytest.main([__file__])
```

---

This integration guide covers the major Python libraries and frameworks you'll commonly use with PyBiorythm. Each example is production-ready and can be adapted for your specific use case.

For more advanced usage patterns, see:
- **[API Reference](../api/)** - Complete method documentation  
- **[Data Analysis Examples](../../examples/)** - Jupyter notebooks with real analysis
- **[Performance Guide](../reference/performance.md)** - Optimization for large datasets