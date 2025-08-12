# Biorhythm Sample Datasets

Standalone dataset generator for biorhythm analysis examples. This directory contains everything needed to generate sample biorhythm datasets without requiring the broader PyBiorythm library.

## 🚀 Quick Start

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies  
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync

# Generate sample datasets
python sample-data-generator.py --output-dir sample_data
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install pandas

# Generate sample datasets
python sample-data-generator.py --output-dir sample_data
```

### Minimal Usage (JSON only)

```bash
# No dependencies needed - just run with Python
python sample-data-generator.py --output-dir sample_data
# Will generate JSON files only (no pandas required)
```

## 📁 Generated Datasets

The generator creates 5 different biorhythm datasets:

| Dataset | Duration | Use Case | People |
|---------|----------|----------|---------|
| `one_year_1990` | 365 days | Learning basics | 1 |
| `two_years_1985` | 730 days | Trend detection | 1 |
| `quarterly_1995` | 90 days | Quick experiments | 1 |
| `five_years_1980` | 1825 days | Statistical power | 1 |
| `multiple_people_2024` | 365 days | Comparative analysis | 3 |

## 📊 Output Formats

- **JSON**: Complete metadata + timeseries data
- **CSV**: Analysis-ready flat format (requires pandas)

## 🔧 Files in This Directory

- `sample-data-generator.py` - Main generator script (standalone)
- `pyproject.toml` - uv/pip dependency specification
- `README.md` - This file
- `data-dictionary.md` - Field descriptions (generated)

## ⚡ Features

- ✅ **Self-contained**: No PyBiorythm library required
- ✅ **Mathematical fallback**: Uses pure Python sine wave calculations
- ✅ **Flexible dependencies**: Works with or without pandas
- ✅ **uv compatible**: Modern Python package management
- ✅ **Multiple formats**: JSON and CSV export
- ✅ **Rich metadata**: Complete dataset documentation

## 🎯 Usage Examples

### Basic Usage
```bash
python sample-data-generator.py
```

### Custom Output Directory
```bash
python sample-data-generator.py --output-dir my_datasets
```

### CSV Format Only (requires pandas)
```bash
python sample-data-generator.py --format csv
```

### JSON Format Only
```bash
python sample-data-generator.py --format json
```

## 📈 Using Generated Data

### Load JSON Data
```python
import json

with open('sample_data/one_year_1990.json', 'r') as f:
    data = json.load(f)

# Access timeseries
timeseries = data['timeseries']
metadata = data['metadata']
```

### Load CSV Data (if pandas available)
```python
import pandas as pd

df = pd.read_csv('sample_data/one_year_1990.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
```

## 🔄 Integration with Analysis Examples

These datasets are designed to work with the analysis notebooks:
- Copy generated data to notebook directory
- Load using the examples in each notebook
- No modification required - datasets are analysis-ready

## 🎓 Educational Use

Perfect for:
- Learning time series analysis
- Practicing statistical methods
- Testing visualization libraries  
- Demonstrating cyclical data patterns
- Academic coursework and research

The mathematical implementation provides predictable, well-understood cyclical patterns ideal for educational purposes.