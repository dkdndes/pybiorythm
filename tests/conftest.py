#!/usr/bin/env python3
"""
Pytest configuration and shared fixtures.
"""
import pytest
from datetime import datetime
from biorythm import BiorhythmCalculator


@pytest.fixture
def sample_birthdate():
    """Common birthdate for testing."""
    return datetime(1990, 5, 15)


@pytest.fixture
def sample_plot_date():
    """Common plot date for testing."""
    return datetime(2025, 8, 7)


@pytest.fixture
def basic_calculator():
    """Basic calculator instance for testing."""
    return BiorhythmCalculator(width=30, days=10, orientation="vertical")


@pytest.fixture
def json_calculator():
    """Calculator optimized for JSON output testing."""
    return BiorhythmCalculator(width=20, days=30, orientation="vertical")


@pytest.fixture
def sample_json_data(json_calculator, sample_birthdate):
    """Sample JSON data for testing."""
    return json_calculator.generate_timeseries_json(sample_birthdate)


@pytest.fixture
def multiple_birthdates():
    """Multiple birthdates for comparative testing."""
    return [
        datetime(1970, 1, 1),
        datetime(1980, 6, 15),
        datetime(1990, 12, 31),
        datetime(2000, 3, 20),
    ]


@pytest.fixture(scope="session")
def large_dataset():
    """Large dataset for performance testing."""
    calc = BiorhythmCalculator(days=365)
    birthdate = datetime(1985, 7, 4)
    return calc.generate_timeseries_json(birthdate)