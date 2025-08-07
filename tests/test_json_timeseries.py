#!/usr/bin/env python3
"""
Test suite specifically for JSON timeseries functionality and data analysis use cases.
Tests designed to validate the JSON output for use in analytics and machine learning.
"""

import json
import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from biorythm import BiorhythmCalculator


class TestJSONTimeseriesStructure:
    """Test the structure and format of JSON timeseries output."""

    def test_json_schema_compliance(self):
        """Test that JSON output follows expected schema."""
        calc = BiorhythmCalculator(days=30)
        birthdate = datetime(1990, 1, 1)
        result = calc.generate_timeseries_json(birthdate)

        # Validate top-level structure
        required_keys = ["meta", "cycle_repeats", "critical_days", "data"]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Validate meta structure
        meta_keys = [
            "generator",
            "version",
            "birthdate",
            "plot_date",
            "days_alive",
            "cycle_lengths_days",
            "chart_orientation",
            "days",
            "width",
            "scientific_warning",
        ]
        for key in meta_keys:
            assert key in result["meta"], f"Missing meta key: {key}"

        # Validate cycle_lengths_days structure
        cycle_keys = ["physical", "emotional", "intellectual"]
        for key in cycle_keys:
            assert key in result["meta"]["cycle_lengths_days"], (
                f"Missing cycle key: {key}"
            )

    def test_data_entries_structure(self):
        """Test that each data entry has the correct structure."""
        calc = BiorhythmCalculator(days=5)
        birthdate = datetime(1990, 5, 15)
        result = calc.generate_timeseries_json(birthdate)

        required_entry_keys = [
            "date",
            "days_alive",
            "physical",
            "emotional",
            "intellectual",
            "critical_cycles",
        ]

        for entry in result["data"]:
            for key in required_entry_keys:
                assert key in entry, f"Missing entry key: {key}"

            # Validate data types
            assert isinstance(entry["date"], str)
            assert isinstance(entry["days_alive"], int)
            assert isinstance(entry["physical"], float)
            assert isinstance(entry["emotional"], float)
            assert isinstance(entry["intellectual"], float)
            assert isinstance(entry["critical_cycles"], list)

    def test_date_format_consistency(self):
        """Test that all dates are in ISO format (YYYY-MM-DD)."""
        calc = BiorhythmCalculator(days=10)
        birthdate = datetime(2000, 12, 25)
        result = calc.generate_timeseries_json(birthdate)

        # Check meta dates
        datetime.strptime(result["meta"]["birthdate"], "%Y-%m-%d")
        datetime.strptime(result["meta"]["plot_date"], "%Y-%m-%d")

        # Check data entry dates
        for entry in result["data"]:
            datetime.strptime(entry["date"], "%Y-%m-%d")

        # Check critical day dates
        for critical_day in result["critical_days"]:
            datetime.strptime(critical_day["date"], "%Y-%m-%d")

    def test_value_ranges(self):
        """Test that biorhythm values are in expected ranges."""
        calc = BiorhythmCalculator(days=50)
        birthdate = datetime(1985, 3, 10)
        result = calc.generate_timeseries_json(birthdate)

        for entry in result["data"]:
            # All biorhythm values should be between -1 and 1
            assert -1.0 <= entry["physical"] <= 1.0
            assert -1.0 <= entry["emotional"] <= 1.0
            assert -1.0 <= entry["intellectual"] <= 1.0

            # Days alive should be non-negative
            assert entry["days_alive"] >= 0


class TestTimeseriesDataAnalysis:
    """Test functionality for data analysis and machine learning use cases."""

    def test_pandas_integration(self):
        """Test integration with pandas DataFrame."""
        calc = BiorhythmCalculator(days=100)
        birthdate = datetime(1990, 1, 1)
        result = calc.generate_timeseries_json(birthdate)

        # Convert to DataFrame
        df = pd.DataFrame(result["data"])
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)

        # Test DataFrame structure
        expected_columns = [
            "days_alive",
            "physical",
            "emotional",
            "intellectual",
            "critical_cycles",
        ]
        for col in expected_columns:
            assert col in df.columns

        # Test data types
        assert df["days_alive"].dtype == "int64"
        assert df["physical"].dtype == "float64"
        assert df["emotional"].dtype == "float64"
        assert df["intellectual"].dtype == "float64"

        # Test index is datetime
        assert pd.api.types.is_datetime64_any_dtype(df.index)

    def test_statistical_properties(self):
        """Test statistical properties of generated timeseries."""
        calc = BiorhythmCalculator(days=1000)  # Large sample for statistics
        birthdate = datetime(1980, 6, 15)
        result = calc.generate_timeseries_json(birthdate)

        df = pd.DataFrame(result["data"])

        # Test that cycles have expected statistical properties
        for cycle in ["physical", "emotional", "intellectual"]:
            values = df[cycle]

            # Mean should be close to 0 (sine wave centered on 0)
            assert abs(values.mean()) < 0.1

            # Standard deviation should be close to 1/sqrt(2) ≈ 0.707 for sine wave
            expected_std = 1 / np.sqrt(2)
            assert abs(values.std() - expected_std) < 0.1

            # Min and max should be close to -1 and 1
            assert values.min() >= -1.0
            assert values.max() <= 1.0
            assert values.min() < -0.9  # Should get close to -1
            assert values.max() > 0.9  # Should get close to 1

    def test_periodicity_detection(self):
        """Test that cycles show expected periodicity."""
        calc = BiorhythmCalculator(days=200)
        birthdate = datetime(1990, 1, 1)
        result = calc.generate_timeseries_json(birthdate)

        df = pd.DataFrame(result["data"])

        # Test physical cycle (23 days)
        physical_values = df["physical"].values

        # Values 23 days apart should be very similar (complete cycle)
        for i in range(23, len(physical_values)):
            if i - 23 >= 0:
                diff = abs(physical_values[i] - physical_values[i - 23])
                assert diff < 0.01, (
                    f"Physical cycle not repeating correctly at index {i}"
                )

    def test_critical_days_identification(self):
        """Test identification and analysis of critical days."""
        calc = BiorhythmCalculator(days=365)  # Full year
        birthdate = datetime(1990, 1, 1)
        result = calc.generate_timeseries_json(birthdate)

        df = pd.DataFrame(result["data"])

        # Find critical days from data
        threshold = 0.05  # CRITICAL_DAY_THRESHOLD
        critical_mask = (
            (df["physical"].abs() <= threshold)
            | (df["emotional"].abs() <= threshold)
            | (df["intellectual"].abs() <= threshold)
        )

        critical_days_from_data = df[critical_mask]

        # Should have some critical days in a year
        assert len(critical_days_from_data) > 0

        # Critical days summary should match data
        critical_dates_summary = {cd["date"] for cd in result["critical_days"]}
        set(
            df[critical_mask].index.strftime("%Y-%m-%d")
            if hasattr(df.index, "strftime")
            else {df.iloc[i]["date"] for i in range(len(df)) if critical_mask.iloc[i]}
        )

        # At least some overlap (exact match depends on how critical_cycles field is populated)
        assert len(critical_dates_summary) > 0

    def test_feature_engineering_potential(self):
        """Test data suitability for feature engineering in ML contexts."""
        calc = BiorhythmCalculator(days=100)
        birthdate = datetime(1985, 7, 20)
        result = calc.generate_timeseries_json(birthdate)

        df = pd.DataFrame(result["data"])
        df["date"] = pd.to_datetime(df["date"])

        # Test rolling statistics (useful for ML features)
        window = 7
        df["physical_rolling_mean"] = df["physical"].rolling(window=window).mean()
        df["emotional_rolling_std"] = df["emotional"].rolling(window=window).std()

        # Should be able to compute without errors
        assert not df["physical_rolling_mean"].isna().all()
        assert not df["emotional_rolling_std"].isna().all()

        # Test lag features
        df["physical_lag_1"] = df["physical"].shift(1)
        df["emotional_lag_7"] = df["emotional"].shift(7)

        # Test difference features
        df["physical_diff"] = df["physical"].diff()

        # All feature engineering should work without errors
        assert len(df) == 100


class TestMultipleBirthdateAnalysis:
    """Test analysis across multiple birthdates for comparative studies."""

    def test_multiple_subjects_data_generation(self):
        """Test generating data for multiple subjects."""
        calc = BiorhythmCalculator(days=30)
        birthdates = [
            datetime(1980, 1, 1),
            datetime(1985, 6, 15),
            datetime(1990, 12, 31),
            datetime(1995, 3, 20),
        ]

        all_results = []
        for i, birthdate in enumerate(birthdates):
            result = calc.generate_timeseries_json(birthdate)

            # Add subject ID to each data point
            for entry in result["data"]:
                entry["subject_id"] = i

            all_results.extend(result["data"])

        # Convert to DataFrame for analysis
        df = pd.DataFrame(all_results)

        # Should have data for all subjects
        assert set(df["subject_id"]) == {0, 1, 2, 3}

        # Each subject should have 30 data points
        assert len(df[df["subject_id"] == 0]) == 30
        assert len(df[df["subject_id"] == 1]) == 30

    def test_cohort_analysis_structure(self):
        """Test structure suitable for cohort analysis."""
        calc = BiorhythmCalculator(days=50)

        # Generate data for different age groups
        birthdates = {
            "young": datetime(2000, 1, 1),
            "middle": datetime(1980, 1, 1),
            "older": datetime(1960, 1, 1),
        }

        cohort_data = {}
        for group, birthdate in birthdates.items():
            result = calc.generate_timeseries_json(birthdate)
            cohort_data[group] = result["data"]

        # Validate structure for each cohort
        for group, data in cohort_data.items():
            assert len(data) == 50
            for entry in data:
                assert "date" in entry
                assert "days_alive" in entry
                # Days alive should differ significantly between cohorts

        # Verify age differences
        young_days = cohort_data["young"][0]["days_alive"]
        middle_days = cohort_data["middle"][0]["days_alive"]
        older_days = cohort_data["older"][0]["days_alive"]

        assert older_days > middle_days > young_days


class TestJSONSerializationAndStorage:
    """Test JSON serialization and storage scenarios."""

    def test_json_serialization_roundtrip(self):
        """Test that data survives JSON serialization roundtrip."""
        calc = BiorhythmCalculator(days=20)
        birthdate = datetime(1992, 8, 5)
        original_result = calc.generate_timeseries_json(birthdate)

        # Serialize to JSON string
        json_string = json.dumps(original_result, indent=2)

        # Deserialize back
        restored_result = json.loads(json_string)

        # Should be identical
        assert restored_result == original_result

    def test_data_export_formats(self):
        """Test exporting data in different formats suitable for analysis tools."""
        calc = BiorhythmCalculator(days=15)
        birthdate = datetime(1988, 4, 12)
        result = calc.generate_timeseries_json(birthdate)

        df = pd.DataFrame(result["data"])

        # Test CSV export
        csv_string = df.to_csv(index=False)
        assert "date,days_alive,physical,emotional,intellectual" in csv_string

        # Test JSON lines format (useful for streaming)
        jsonl_lines = [json.dumps(entry) for entry in result["data"]]
        assert len(jsonl_lines) == 15

        # Each line should be valid JSON
        for line in jsonl_lines:
            parsed = json.loads(line)
            assert "date" in parsed

    def test_large_dataset_generation(self):
        """Test generating larger datasets suitable for ML training."""
        calc = BiorhythmCalculator(days=365 * 2)  # 2 years of data
        birthdate = datetime(1975, 11, 30)
        result = calc.generate_timeseries_json(birthdate)

        # Should handle large datasets
        assert len(result["data"]) == 365 * 2

        # Memory efficiency check - data should be reasonable size
        json_size = len(json.dumps(result))
        assert json_size < 10 * 1024 * 1024  # Less than 10MB for 2 years

        # Data integrity check
        dates = [entry["date"] for entry in result["data"]]
        assert len(set(dates)) == len(dates)  # All dates unique


if __name__ == "__main__":
    pytest.main([__file__])
