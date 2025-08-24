# conftest.py
#!/usr/bin/env python3
"""
Pytest configuration:
- Auto-tag test modules (unit/integration/e2e/json/examples)
- Skip slow/network tests unless explicitly allowed
- Ignore docs/site/example trees during collection (belt + suspenders)
- Shared fixtures for common dates and calculators
"""

from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime
import pytest

# ---- Collection guards -------------------------------------------------------

_IGNORE_DIRS = {"docs", "site", "examples"}

def pytest_ignore_collect(path, config):  # pragma: no cover
    p = Path(str(path))
    return any(part in _IGNORE_DIRS for part in p.parts)

# ---- CLI options & default skipping ------------------------------------------

def pytest_addoption(parser):  # pragma: no cover
    group = parser.getgroup("biorythm")
    group.addoption(
        "--runslow",
        action="store_true",
        default=False,
        help="Run tests marked as slow.",
    )
    group.addoption(
        "--network",
        action="store_true",
        default=False,
        help="Run tests that need internet/network.",
    )

def pytest_collection_modifyitems(config, items):
    """Auto-apply markers by filename and enforce default skips."""
    runslow = config.getoption("--runslow")
    runnet = config.getoption("--network")

    slow_skip = pytest.mark.skip(reason="use --runslow to run")
    net_skip = pytest.mark.skip(reason="use --network to run")

    # Auto-tagging by filename → helps targeted runs without editing each test
    AUTO_MARK = {
        "test_biorhythm_calculator.py": pytest.mark.unit,
        "test_json_timeseries.py": pytest.mark.json,
        "test_main.py": pytest.mark.e2e,
        "test_biorythm_coverage.py": pytest.mark.integration,
        # If you ever purposely keep example tests:
        "test_biorhythm.py": pytest.mark.examples,
    }

    for item in items:
        fname = os.path.basename(str(item.fspath))
        if fname in AUTO_MARK:
            item.add_marker(AUTO_MARK[fname])

        # Respect explicit markers
        if "slow" in item.keywords and not runslow:
            item.add_marker(slow_skip)
        if "network" in item.keywords and not runnet:
            item.add_marker(net_skip)

# ---- Shared fixtures ---------------------------------------------------------

@pytest.fixture
def sample_birthdate() -> datetime:
    """Common birthdate for testing."""
    return datetime(1990, 5, 15)

@pytest.fixture
def sample_plotdate() -> datetime:
    """Common plot date for testing."""
    return datetime(2024, 2, 15)

@pytest.fixture
def calculator():
    """Default calculator for unit tests."""
    from biorythm import BiorhythmCalculator
    return BiorhythmCalculator()

@pytest.fixture
def json_calculator():
    """Calculator optimised for JSON/analytics tests."""
    from biorythm import BiorhythmCalculator
    return BiorhythmCalculator(width=20, days=30, orientation="vertical")

@pytest.fixture
def sample_json_data(json_calculator, sample_birthdate):
    """Generated JSON for schema/analytics tests."""
    return json_calculator.generate_timeseries_json(sample_birthdate)

@pytest.fixture
def multiple_birthdates():
    """Multiple birthdates for comparative tests."""
    return [
        datetime(1980, 1, 1),
        datetime(1990, 5, 15),
        datetime(2000, 12, 31),
    ]
