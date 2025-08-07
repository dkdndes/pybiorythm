#!/usr/bin/env python3
"""
Test suite for BiorhythmCalculator class.
"""

import json
import math
import pytest
from datetime import datetime

from biorythm import (
    BiorhythmCalculator,
    DateValidator,
    DateValidationError,
    ChartParameterError,
    PHYSICAL_CYCLE_DAYS,
    EMOTIONAL_CYCLE_DAYS,
    INTELLECTUAL_CYCLE_DAYS,
    CRITICAL_DAY_THRESHOLD,
)


class TestBiorhythmCalculator:
    """Test cases for BiorhythmCalculator class."""

    def test_init_default_parameters(self):
        """Test calculator initialization with default parameters."""
        calc = BiorhythmCalculator()
        assert calc.width == 55
        assert calc.days == 29
        assert calc.orientation == "vertical"
        assert calc.midwidth == 27
        assert calc.middays == 14

    def test_init_custom_parameters(self):
        """Test calculator initialization with custom parameters."""
        calc = BiorhythmCalculator(width=80, days=60, orientation="horizontal")
        assert calc.width == 80
        assert calc.days == 60
        assert calc.orientation == "horizontal"
        assert calc.midwidth == 40
        assert calc.middays == 30

    def test_init_minimum_width_enforcement(self):
        """Test that minimum width is enforced."""
        calc = BiorhythmCalculator(width=5)
        assert calc.width == 12  # MIN_CHART_WIDTH

    def test_init_invalid_orientation(self):
        """Test that invalid orientation raises error."""
        with pytest.raises(ChartParameterError):
            BiorhythmCalculator(orientation="invalid")

    def test_init_invalid_parameters(self):
        """Test that invalid parameters raise errors."""
        with pytest.raises(ChartParameterError):
            BiorhythmCalculator(width=-1)

        with pytest.raises(ChartParameterError):
            BiorhythmCalculator(days=0)

        with pytest.raises(ChartParameterError):
            BiorhythmCalculator(width="not_an_int")

    def test_calculate_biorhythm_values_known_case(self):
        """Test biorhythm calculation for a known case."""
        calc = BiorhythmCalculator()
        birthdate = datetime(1990, 1, 1)
        target_date = datetime(1990, 1, 24)  # 23 days later

        physical, emotional, intellectual = calc.calculate_biorhythm_values(
            birthdate, target_date
        )

        # After exactly 23 days, physical cycle should complete one full cycle (sin(2π) = 0)
        assert abs(physical) < 0.001
        # After 23 days: emotional = sin(2π * 23/28), intellectual = sin(2π * 23/33)
        assert abs(emotional - math.sin(2 * math.pi * 23 / 28)) < 0.001
        assert abs(intellectual - math.sin(2 * math.pi * 23 / 33)) < 0.001

    def test_calculate_biorhythm_values_same_date(self):
        """Test biorhythm values on birth date (0 days alive)."""
        calc = BiorhythmCalculator()
        birthdate = datetime(1990, 5, 15)

        physical, emotional, intellectual = calc.calculate_biorhythm_values(
            birthdate, birthdate
        )

        # All cycles should be at 0 on birth date
        assert physical == 0.0
        assert emotional == 0.0
        assert intellectual == 0.0

    def test_is_critical_day_all_critical(self):
        """Test critical day detection when all cycles are critical."""
        calc = BiorhythmCalculator()
        is_critical, cycles = calc.is_critical_day(0.01, -0.02, 0.03)
        assert is_critical is True
        assert set(cycles) == {"Physical", "Emotional", "Intellectual"}

    def test_is_critical_day_partial_critical(self):
        """Test critical day detection when some cycles are critical."""
        calc = BiorhythmCalculator()
        is_critical, cycles = calc.is_critical_day(0.01, 0.5, -0.03)
        assert is_critical is True
        assert set(cycles) == {"Physical", "Intellectual"}

    def test_is_critical_day_none_critical(self):
        """Test critical day detection when no cycles are critical."""
        calc = BiorhythmCalculator()
        is_critical, cycles = calc.is_critical_day(0.5, -0.7, 0.8)
        assert is_critical is False
        assert cycles == []

    def test_critical_day_threshold(self):
        """Test critical day threshold boundary conditions."""
        calc = BiorhythmCalculator()

        # Exactly at threshold - should be critical
        is_critical, cycles = calc.is_critical_day(CRITICAL_DAY_THRESHOLD, 0.1, 0.1)
        assert is_critical is True
        assert "Physical" in cycles

        # Just above threshold - should not be critical
        is_critical, cycles = calc.is_critical_day(
            CRITICAL_DAY_THRESHOLD + 0.001, 0.1, 0.1
        )
        assert is_critical is False

    def test_generate_timeseries_json_structure(self):
        """Test that JSON output has correct structure."""
        calc = BiorhythmCalculator(days=7)
        birthdate = datetime(1990, 5, 15)
        plot_date = datetime(2025, 8, 7)

        result = calc.generate_timeseries_json(birthdate, plot_date)

        # Check top-level structure
        assert "meta" in result
        assert "cycle_repeats" in result
        assert "critical_days" in result
        assert "data" in result

        # Check meta structure
        meta = result["meta"]
        assert "generator" in meta
        assert "version" in meta
        assert "birthdate" in meta
        assert "plot_date" in meta
        assert "days_alive" in meta
        assert "cycle_lengths_days" in meta
        assert "scientific_warning" in meta

        # Check cycle lengths
        cycles = meta["cycle_lengths_days"]
        assert cycles["physical"] == PHYSICAL_CYCLE_DAYS
        assert cycles["emotional"] == EMOTIONAL_CYCLE_DAYS
        assert cycles["intellectual"] == INTELLECTUAL_CYCLE_DAYS

        # Check data structure
        assert len(result["data"]) == 7
        for entry in result["data"]:
            assert "date" in entry
            assert "days_alive" in entry
            assert "physical" in entry
            assert "emotional" in entry
            assert "intellectual" in entry
            assert "critical_cycles" in entry

    def test_generate_timeseries_json_data_validity(self):
        """Test that JSON data values are mathematically correct."""
        calc = BiorhythmCalculator(days=3)
        birthdate = datetime(1990, 1, 1)
        plot_date = datetime(1990, 1, 2)  # 1 day after birth

        result = calc.generate_timeseries_json(birthdate, plot_date)
        data = result["data"]

        # Check middle entry (plot date, 1 day alive)
        middle_entry = data[1]  # Should be the plot date
        assert middle_entry["days_alive"] == 1

        # Verify calculations match expected values
        expected_physical = math.sin(2 * math.pi * 1 / PHYSICAL_CYCLE_DAYS)
        expected_emotional = math.sin(2 * math.pi * 1 / EMOTIONAL_CYCLE_DAYS)
        expected_intellectual = math.sin(2 * math.pi * 1 / INTELLECTUAL_CYCLE_DAYS)

        assert abs(middle_entry["physical"] - expected_physical) < 0.001
        assert abs(middle_entry["emotional"] - expected_emotional) < 0.001
        assert abs(middle_entry["intellectual"] - expected_intellectual) < 0.001

    def test_generate_timeseries_json_critical_days(self):
        """Test that critical days are correctly identified in JSON output."""
        calc = BiorhythmCalculator(days=100)  # Larger range to catch critical days
        birthdate = datetime(1990, 1, 1)

        result = calc.generate_timeseries_json(birthdate)

        # Verify critical days in data match critical_days summary
        critical_dates_from_data = []
        for entry in result["data"]:
            if entry["critical_cycles"]:
                critical_dates_from_data.append(entry["date"])

        critical_dates_from_summary = [cd["date"] for cd in result["critical_days"]]

        assert set(critical_dates_from_data) == set(critical_dates_from_summary)


class TestDateValidator:
    """Test cases for DateValidator class."""

    def test_validate_date_components_valid(self):
        """Test validation of valid date components."""
        # Should not raise any exceptions
        DateValidator.validate_date_components(1990, 5, 15)
        DateValidator.validate_date_components(1, 1, 1)
        DateValidator.validate_date_components(9999, 12, 31)

    def test_validate_date_components_invalid_year(self):
        """Test validation with invalid years."""
        with pytest.raises(DateValidationError):
            DateValidator.validate_date_components(0, 5, 15)

        with pytest.raises(DateValidationError):
            DateValidator.validate_date_components(10000, 5, 15)

    def test_validate_date_components_invalid_month(self):
        """Test validation with invalid months."""
        with pytest.raises(DateValidationError):
            DateValidator.validate_date_components(1990, 0, 15)

        with pytest.raises(DateValidationError):
            DateValidator.validate_date_components(1990, 13, 15)

    def test_validate_date_components_invalid_day(self):
        """Test validation with invalid days."""
        with pytest.raises(DateValidationError):
            DateValidator.validate_date_components(1990, 5, 0)

        with pytest.raises(DateValidationError):
            DateValidator.validate_date_components(1990, 5, 32)

    def test_create_validated_date_valid(self):
        """Test creation of valid dates."""
        date = DateValidator.create_validated_date(1990, 5, 15)
        assert date == datetime(1990, 5, 15)

    def test_create_validated_date_invalid_date(self):
        """Test creation with impossible date combinations."""
        with pytest.raises(DateValidationError):
            DateValidator.create_validated_date(2021, 2, 30)  # Feb 30 doesn't exist

    def test_create_validated_date_future_date(self):
        """Test that future dates are rejected."""
        future_year = datetime.now().year + 10
        with pytest.raises(DateValidationError):
            DateValidator.create_validated_date(future_year, 1, 1)


class TestChartGeneration:
    """Test cases for chart generation functionality."""

    def test_generate_chart_vertical(self, capsys):
        """Test vertical chart generation produces output."""
        calc = BiorhythmCalculator(width=20, days=5, orientation="vertical")
        birthdate = datetime(1990, 5, 15)

        calc.generate_chart(birthdate)

        captured = capsys.readouterr()
        output = captured.out

        # Should contain header information
        assert "BIORHYTHM CHART (VERTICAL)" in output
        assert "Birth:" in output
        assert "Plot:" in output
        assert "Alive:" in output

        # Should contain legend
        assert "Physical" in output
        assert "Emotional" in output
        assert "Intellectual" in output

    def test_generate_chart_horizontal(self, capsys):
        """Test horizontal chart generation produces output."""
        calc = BiorhythmCalculator(width=30, days=5, orientation="horizontal")
        birthdate = datetime(1990, 5, 15)

        calc.generate_chart(birthdate)

        captured = capsys.readouterr()
        output = captured.out

        # Should contain header information
        assert "BIORHYTHM CHART (HORIZONTAL)" in output
        assert "BIORHYTHM WAVE (all cycles)" in output


class TestUtilityFunctions:
    """Test cases for utility functions and edge cases."""

    def test_cycle_constants(self):
        """Test that cycle constants are correct."""
        assert PHYSICAL_CYCLE_DAYS == 23
        assert EMOTIONAL_CYCLE_DAYS == 28
        assert INTELLECTUAL_CYCLE_DAYS == 33

    def test_critical_threshold_constant(self):
        """Test critical day threshold constant."""
        assert CRITICAL_DAY_THRESHOLD == 0.05

    def test_biorhythm_calculator_with_extreme_values(self):
        """Test calculator with extreme but valid values."""
        # Very old birthdate
        calc = BiorhythmCalculator(days=10)
        old_birthdate = datetime(1900, 1, 1)

        result = calc.generate_timeseries_json(old_birthdate)
        assert "data" in result
        assert len(result["data"]) == 10

    def test_json_serialization(self):
        """Test that JSON output is valid JSON."""
        calc = BiorhythmCalculator(days=5)
        birthdate = datetime(1990, 5, 15)

        result = calc.generate_timeseries_json(birthdate)

        # Should be able to serialize to JSON string and back
        json_str = json.dumps(result)
        parsed = json.loads(json_str)

        assert parsed == result


class TestErrorHandling:
    """Test cases for error handling and edge cases."""

    def test_invalid_chart_parameters_type_errors(self):
        """Test type validation for chart parameters."""
        with pytest.raises(ChartParameterError):
            BiorhythmCalculator(width="invalid")

        with pytest.raises(ChartParameterError):
            BiorhythmCalculator(days="invalid")

    def test_chart_generation_with_invalid_birthdate(self):
        """Test chart generation with problematic dates."""
        calc = BiorhythmCalculator()

        # Test with same date as plot date
        birthdate = datetime(2025, 8, 7)
        plot_date = datetime(2025, 8, 7)

        # Should work (0 days alive)
        result = calc.generate_timeseries_json(birthdate, plot_date)
        assert result["meta"]["days_alive"] == 0


# Fixtures and test data
@pytest.fixture
def sample_birthdate():
    """Fixture providing a sample birthdate."""
    return datetime(1990, 5, 15)


@pytest.fixture
def sample_calculator():
    """Fixture providing a sample calculator instance."""
    return BiorhythmCalculator(width=30, days=10, orientation="vertical")


class TestWithFixtures:
    """Tests using pytest fixtures."""

    def test_calculator_with_sample_data(self, sample_calculator, sample_birthdate):
        """Test calculator with sample data from fixtures."""
        result = sample_calculator.generate_timeseries_json(sample_birthdate)

        assert result["meta"]["birthdate"] == "1990-05-15"
        assert len(result["data"]) == 10

    def test_multiple_calculations_consistency(self, sample_birthdate):
        """Test that multiple calculations with same input are consistent."""
        calc1 = BiorhythmCalculator(days=5)
        calc2 = BiorhythmCalculator(days=5)

        result1 = calc1.generate_timeseries_json(sample_birthdate)
        result2 = calc2.generate_timeseries_json(sample_birthdate)

        # Results should be identical
        assert result1["data"] == result2["data"]


if __name__ == "__main__":
    pytest.main([__file__])
