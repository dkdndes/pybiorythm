#!/usr/bin/env python3
r"""
Sample Biorhythm Dataset Generator

This script generates various sample biorhythm datasets for analysis and experimentation.
Perfect for analysts who want to explore biorhythm patterns without generating data themselves.

## Setup Instructions:

### Using uv (recommended):
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv add pandas

# Run the generator
python sample-data-generator.py --output-dir sample_data
```

### Using pip:
```bash
pip install pandas
python sample-data-generator.py --output-dir sample_data
```

## Standalone Usage:
This script is completely self-contained and includes mathematical fallback implementations.
No PyBiorythm library required - it will work independently.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import math

# Always use mathematical fallback for standalone operation
BIORYTHM_AVAILABLE = False
print("🔄 Using standalone mathematical implementation (no PyBiorythm required)")

# Check for pandas availability
try:
    import pandas as pd

    PANDAS_AVAILABLE = True
    print("✅ pandas available for CSV export")
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠️  pandas not found - JSON export only")
    print("    Install with: uv add pandas  or  pip install pandas")


class BiorhythmCalculator:
    """Fallback implementation for generating sample data."""

    def __init__(self, days=30, width=55, orientation="vertical"):
        self.days = days
        self.width = width
        self.orientation = orientation

    def generate_timeseries_json(self, birthdate, start_date=None):
        if start_date is None:
            start_date = datetime.now()

        timeseries = []
        for i in range(self.days):
            current_date = start_date + timedelta(days=i)
            day_number = (current_date - birthdate).days

            # Calculate cycles using sine waves
            physical = math.sin(2 * math.pi * day_number / 23)
            emotional = math.sin(2 * math.pi * day_number / 28)
            intellectual = math.sin(2 * math.pi * day_number / 33)

            # Detect critical days (near zero crossings)
            critical_days = []
            if abs(physical) < 0.05:
                critical_days.append(
                    "physical_" + ("positive" if physical >= 0 else "negative")
                )
            if abs(emotional) < 0.05:
                critical_days.append(
                    "emotional_" + ("positive" if emotional >= 0 else "negative")
                )
            if abs(intellectual) < 0.05:
                critical_days.append(
                    "intellectual_" + ("positive" if intellectual >= 0 else "negative")
                )

            entry = {
                "date": current_date.strftime("%Y-%m-%d"),
                "day_number": day_number,
                "cycles": {
                    "physical": round(physical, 6),
                    "emotional": round(emotional, 6),
                    "intellectual": round(intellectual, 6),
                },
                "critical_days": critical_days,
            }
            timeseries.append(entry)

        return {
            "metadata": {
                "birthdate": birthdate.strftime("%Y-%m-%d"),
                "chart_start_date": start_date.strftime("%Y-%m-%d"),
                "chart_period_days": self.days,
                "generation_timestamp": datetime.now().isoformat(),
                "cycles": {
                    "physical": {"period_days": 23, "description": "Physical cycle"},
                    "emotional": {"period_days": 28, "description": "Emotional cycle"},
                    "intellectual": {
                        "period_days": 33,
                        "description": "Intellectual cycle",
                    },
                },
            },
            "timeseries": timeseries,
        }


def generate_sample_datasets():
    """Generate various sample datasets for different analysis scenarios."""

    datasets = {}

    # Dataset 1: One Year Analysis (Popular birthdate)
    print("Generating Dataset 1: One Year Analysis...")
    calc = BiorhythmCalculator(days=365)
    birthdate = datetime(1990, 5, 15)  # Popular example birthdate
    start_date = datetime(2024, 1, 1)

    data = calc.generate_timeseries_json(birthdate, start_date)
    datasets["one_year_1990"] = data

    # Dataset 2: Two Years Analysis (Different birthdate)
    print("Generating Dataset 2: Two Year Analysis...")
    calc = BiorhythmCalculator(days=730)
    birthdate = datetime(1985, 3, 22)
    start_date = datetime(2023, 1, 1)

    data = calc.generate_timeseries_json(birthdate, start_date)
    datasets["two_years_1985"] = data

    # Dataset 3: Short Term Analysis (90 days)
    print("Generating Dataset 3: Quarterly Analysis...")
    calc = BiorhythmCalculator(days=90)
    birthdate = datetime(1995, 8, 10)
    start_date = datetime(2024, 1, 1)

    data = calc.generate_timeseries_json(birthdate, start_date)
    datasets["quarterly_1995"] = data

    # Dataset 4: Long Term Analysis (5 years)
    print("Generating Dataset 4: Five Year Analysis...")
    calc = BiorhythmCalculator(days=1825)  # 5 years
    birthdate = datetime(1980, 12, 25)
    start_date = datetime(2020, 1, 1)

    data = calc.generate_timeseries_json(birthdate, start_date)
    datasets["five_years_1980"] = data

    # Dataset 5: Multiple People Comparison
    print("Generating Dataset 5: Multiple People...")
    people_data = {}
    birthdates = [
        ("person_a", datetime(1990, 1, 15)),
        ("person_b", datetime(1990, 6, 15)),
        ("person_c", datetime(1990, 12, 15)),
    ]

    calc = BiorhythmCalculator(days=365)
    start_date = datetime(2024, 1, 1)

    for person_id, birthdate in birthdates:
        data = calc.generate_timeseries_json(birthdate, start_date)
        people_data[person_id] = data

    datasets["multiple_people_2024"] = people_data

    return datasets


def export_to_csv(json_data, filename):
    """Convert JSON biorhythm data to CSV format."""

    if not PANDAS_AVAILABLE:
        print(f"⚠️  Skipping CSV export for {filename} - pandas not available")
        return 0

    try:
        # Handle multiple people dataset
        if isinstance(json_data, dict) and "metadata" not in json_data:
            # This is a multiple people dataset
            all_dataframes = []
            for person_id, person_data in json_data.items():
                df = pd.json_normalize(person_data["timeseries"])
                df["person_id"] = person_id
                df["birthdate"] = person_data["metadata"]["birthdate"]
                all_dataframes.append(df)

            combined_df = pd.concat(all_dataframes, ignore_index=True)
            combined_df.to_csv(filename, index=False)
            return len(combined_df)

        else:
            # Single person dataset
            df = pd.json_normalize(json_data["timeseries"])
            df.to_csv(filename, index=False)
            return len(df)

    except Exception as e:
        print(f"⚠️  CSV export failed for {filename}: {e}")
        return 0


def create_analysis_ready_files(datasets, output_dir):
    """Create analysis-ready files in various formats."""

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    files_created = []

    for dataset_name, data in datasets.items():
        # JSON format (complete data)
        json_file = output_path / f"{dataset_name}.json"
        with open(json_file, "w") as f:
            json.dump(data, f, indent=2, default=str)
        files_created.append(str(json_file))

        # CSV format (timeseries only) - only if pandas available
        if PANDAS_AVAILABLE:
            csv_file = output_path / f"{dataset_name}.csv"
            row_count = export_to_csv(data, csv_file)
            if row_count > 0:
                files_created.append(str(csv_file))
            print(f"Created {dataset_name}: JSON + CSV ({row_count} rows)")
        else:
            # Count rows from JSON data for reporting
            if isinstance(data, dict) and "timeseries" in data:
                row_count = len(data["timeseries"])
            elif isinstance(data, dict):
                # Multiple people dataset
                row_count = sum(
                    len(person_data.get("timeseries", []))
                    for person_data in data.values()
                    if isinstance(person_data, dict)
                )
            else:
                row_count = 0
            print(f"Created {dataset_name}: JSON only ({row_count} rows)")

    return files_created


def create_data_dictionary():
    """Create a comprehensive data dictionary."""

    data_dictionary = {
        "overview": {
            "description": "Biorhythm sample datasets for analysis and experimentation",
            "source": "Generated using PyBiorythm library",
            "license": "MIT License - Free for educational and commercial use",
            "scientific_disclaimer": "Biorhythm theory is considered pseudoscience. Data provided for educational purposes only.",
        },
        "datasets": {
            "one_year_1990": {
                "description": "One year of biorhythm data for person born 1990-05-15",
                "period": "2024-01-01 to 2024-12-31",
                "rows": 365,
                "use_cases": [
                    "Basic time series analysis",
                    "Seasonal pattern detection",
                    "Statistical learning",
                ],
            },
            "two_years_1985": {
                "description": "Two years of biorhythm data for person born 1985-03-22",
                "period": "2023-01-01 to 2024-12-30",
                "rows": 730,
                "use_cases": [
                    "Long-term trend analysis",
                    "Cycle validation",
                    "Advanced statistics",
                ],
            },
            "quarterly_1995": {
                "description": "90 days of biorhythm data for person born 1995-08-10",
                "period": "2024-01-01 to 2024-03-30",
                "rows": 90,
                "use_cases": [
                    "Quick analysis",
                    "Visualization practice",
                    "Algorithm testing",
                ],
            },
            "five_years_1980": {
                "description": "Five years of biorhythm data for person born 1980-12-25",
                "period": "2020-01-01 to 2024-12-30",
                "rows": 1825,
                "use_cases": [
                    "Big data analysis",
                    "Machine learning",
                    "Performance testing",
                ],
            },
            "multiple_people_2024": {
                "description": "Comparative data for 3 people born in different months of 1990",
                "period": "2024-01-01 to 2024-12-31",
                "rows": 1095,
                "use_cases": [
                    "Comparative analysis",
                    "Group studies",
                    "Cohort analysis",
                ],
            },
        },
        "data_structure": {
            "json_format": {
                "metadata": {
                    "birthdate": "Birth date in YYYY-MM-DD format",
                    "chart_start_date": "First date in dataset",
                    "chart_period_days": "Number of days included",
                    "generation_timestamp": "When dataset was created",
                    "cycles": "Information about the three biorhythm cycles",
                },
                "timeseries": {
                    "date": "Date in YYYY-MM-DD format",
                    "day_number": "Days since birth",
                    "cycles": {
                        "physical": "Physical cycle value (-1.0 to +1.0)",
                        "emotional": "Emotional cycle value (-1.0 to +1.0)",
                        "intellectual": "Intellectual cycle value (-1.0 to +1.0)",
                    },
                    "critical_days": "List of critical day events (cycle zero crossings)",
                },
            },
            "csv_format": {
                "date": "Date in YYYY-MM-DD format",
                "day_number": "Days since birth (integer)",
                "cycles.physical": "Physical cycle value (float, -1.0 to +1.0)",
                "cycles.emotional": "Emotional cycle value (float, -1.0 to +1.0)",
                "cycles.intellectual": "Intellectual cycle value (float, -1.0 to +1.0)",
                "critical_days": "JSON array of critical day events",
                "person_id": "Person identifier (for multi-person datasets)",
                "birthdate": "Birth date (for multi-person datasets)",
            },
        },
        "cycle_information": {
            "physical_cycle": {
                "period_days": 23,
                "description": "Affects physical strength, endurance, and energy levels",
                "formula": "sin(2π × day_number / 23)",
            },
            "emotional_cycle": {
                "period_days": 28,
                "description": "Affects mood, creativity, and emotional sensitivity",
                "formula": "sin(2π × day_number / 28)",
            },
            "intellectual_cycle": {
                "period_days": 33,
                "description": "Affects mental acuity, logic, and reasoning ability",
                "formula": "sin(2π × day_number / 33)",
            },
        },
        "analysis_suggestions": {
            "descriptive_statistics": "Calculate mean, std, min, max for each cycle",
            "correlation_analysis": "Examine relationships between cycles",
            "time_series_plots": "Visualize cycles over time",
            "critical_day_analysis": "Study zero-crossing patterns",
            "seasonal_patterns": "Look for monthly or weekly patterns",
            "frequency_analysis": "Validate cycle periods using FFT",
            "comparative_analysis": "Compare cycles between different people",
            "trend_analysis": "Examine long-term patterns using moving averages",
        },
    }

    return data_dictionary


def main():
    parser = argparse.ArgumentParser(
        description="Generate sample biorhythm datasets for analysis"
    )
    parser.add_argument(
        "--output-dir",
        default="sample_datasets",
        help="Output directory for generated datasets",
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv", "both"],
        default="both",
        help="Output format for datasets",
    )

    args = parser.parse_args()

    print("PyBiorythm Sample Dataset Generator")
    print("=" * 40)
    print(f"Biorythm package available: {BIORYTHM_AVAILABLE}")
    print(f"Output directory: {args.output_dir}")
    print(f"Output format: {args.format}")
    print()

    # Generate datasets
    print("Generating sample datasets...")
    datasets = generate_sample_datasets()

    # Create output files
    print(f"\nCreating output files in {args.output_dir}/...")
    files_created = create_analysis_ready_files(datasets, args.output_dir)

    # Create data dictionary
    print("Creating data dictionary...")
    data_dict = create_data_dictionary()

    dict_file = Path(args.output_dir) / "data_dictionary.json"
    with open(dict_file, "w") as f:
        json.dump(data_dict, f, indent=2)
    files_created.append(str(dict_file))

    # Create README for datasets
    readme_content = """# Biorhythm Sample Datasets

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
"""

    readme_file = Path(args.output_dir) / "README.md"
    with open(readme_file, "w") as f:
        f.write(readme_content)
    files_created.append(str(readme_file))

    # Summary
    print("\n✅ Dataset generation complete!")
    print(f"Files created: {len(files_created)}")
    for file in files_created:
        print(f"  - {file}")

    print("\n📊 Ready for analysis!")
    print(
        f"Total data points generated: {sum(len(d.get('timeseries', [])) if isinstance(d, dict) and 'timeseries' in d else sum(len(sub_d.get('timeseries', [])) for sub_d in d.values() if isinstance(sub_d, dict)) for d in datasets.values())}"
    )


if __name__ == "__main__":
    main()
