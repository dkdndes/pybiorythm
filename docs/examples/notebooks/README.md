# Biorhythm Analysis Notebooks

Standalone Jupyter notebooks for comprehensive biorhythm data analysis. Each notebook is self-contained and includes mathematical fallback implementations.

## 🚀 Quick Setup

### Using uv (Recommended)

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup environment with all dependencies
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv sync --all-extras

# Start Jupyter
uv run jupyter lab
# or
uv run jupyter notebook
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install core dependencies
pip install pandas numpy matplotlib seaborn scipy jupyter

# Install optional dependencies for advanced features  
pip install plotly bokeh ipywidgets statsmodels scikit-learn

# Start Jupyter
jupyter lab
```

### Minimal Setup (Basic Analysis Only)

```bash
pip install pandas numpy matplotlib jupyter
jupyter notebook
```

## 📓 Available Notebooks

### 🔬 [biorhythm-analysis.ipynb](biorhythm-analysis.ipynb)
**Complete end-to-end analysis workflow**

**What you'll accomplish:**
- Statistical analysis of biorhythm time series
- Data validation and quality assessment
- Critical day analysis and visualization
- Export results for further research

**Dependencies:** pandas, numpy, matplotlib, seaborn
**Duration:** 15-20 minutes to run

---

### 📊 [correlation-study.ipynb](correlation-study.ipynb)
**Advanced statistical correlation analysis**

**What you'll discover:**
- Cross-correlation between different cycles
- Autocorrelation validation of periods
- Statistical significance testing
- Rolling correlation patterns

**Dependencies:** pandas, numpy, scipy, matplotlib, seaborn, statsmodels
**Duration:** 25-30 minutes to run

---

### 🎨 [visualization-gallery.ipynb](visualization-gallery.ipynb)
**Chart examples with multiple libraries**

**What you'll create:**
- Publication-quality static plots
- Interactive visualizations  
- Statistical plots and dashboards
- Export-ready figures

**Dependencies:** pandas, numpy, matplotlib, seaborn, plotly, bokeh
**Duration:** 20-25 minutes to run

## 🔧 Standalone Features

All notebooks include:

- ✅ **Self-contained mathematical implementations**
- ✅ **No PyBiorythm library required**  
- ✅ **Automatic dependency checking**
- ✅ **Fallback implementations for missing packages**
- ✅ **Clear installation instructions**
- ✅ **Rich educational explanations**

## 🎯 Running Individual Notebooks

Each notebook can be run independently:

```bash
# For basic analysis
pip install pandas numpy matplotlib seaborn jupyter
jupyter notebook biorhythm-analysis.ipynb

# For correlation study  
pip install pandas numpy scipy matplotlib seaborn statsmodels jupyter
jupyter notebook correlation-study.ipynb

# For visualization gallery
pip install pandas numpy matplotlib seaborn plotly jupyter  
jupyter notebook visualization-gallery.ipynb
```

## 📊 Using with Sample Data

### Option 1: Generate Data in Notebook
Each notebook includes data generation code - just run all cells.

### Option 2: Use Pre-generated Data
```bash
# Generate sample datasets first
cd ../datasets
python sample-data-generator.py --output-dir ../notebooks/sample_data

# Then load in notebooks
import pandas as pd
df = pd.read_csv('sample_data/one_year_1990.csv')
```

## 🎓 Learning Path

### Beginner: New to Biorhythm Analysis
1. Start with **biorhythm-analysis.ipynb**
2. Explore **visualization-gallery.ipynb** 
3. Try **correlation-study.ipynb** for advanced techniques

### Advanced: Experienced with Time Series
1. Jump to **correlation-study.ipynb** for statistical methods
2. Use **visualization-gallery.ipynb** for presentation-quality plots
3. Refer to **biorhythm-analysis.ipynb** for workflow templates

### Researcher: Academic/Scientific Use
1. **correlation-study.ipynb** - Statistical validation methods
2. **biorhythm-analysis.ipynb** - Complete methodology documentation  
3. **visualization-gallery.ipynb** - Publication-ready figures

## 🔄 Customization

Each notebook is designed to be easily customized:

- Change birth dates and analysis periods
- Modify statistical parameters
- Add your own analysis techniques
- Export results in different formats
- Integrate with your existing workflows

## 🚨 Troubleshooting

### Missing Dependencies
Notebooks will show clear error messages with installation instructions for missing packages.

### Memory Issues
For large datasets (>5 years), consider:
- Using smaller date ranges
- Reducing visualization complexity
- Running analysis in chunks

### Jupyter Issues
```bash
# Reset Jupyter kernel
# In notebook: Kernel → Restart & Clear Output

# Update Jupyter
uv add --upgrade jupyter
# or
pip install --upgrade jupyter
```

## 📈 Integration Examples

### Export to R
```python
# In notebook
df.to_csv('biorhythm_data.csv', index=False)
# Load in R: data <- read.csv('biorhythm_data.csv')
```

### Export to Excel
```python
# In notebook  
df.to_excel('biorhythm_analysis.xlsx', index=False)
```

### Use in Other Projects
```python
# Copy generated analysis functions
from biorhythm_analysis import analyze_cycles
results = analyze_cycles(your_data)
```

Perfect for coursework, research projects, and portfolio demonstrations!