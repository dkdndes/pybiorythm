"""
Biorythm calculation library.

A Python library for generating biorhythm charts and timeseries data
based on the pseudoscientific biorhythm theory.

WARNING: This software implements biorhythm theory, which is considered
PSEUDOSCIENCE. This implementation is provided FOR ENTERTAINMENT PURPOSES ONLY.
"""

from .core import (
    BiorhythmCalculator,
    DateValidator,
    UserInterface,
    BiorhythmError,
    DateValidationError,
    ChartParameterError,
    main,
    setup_logging,
    MIN_YEAR,
    MAX_YEAR,
    CRITICAL_DAY_THRESHOLD,
    PHYSICAL_CYCLE_DAYS,
    EMOTIONAL_CYCLE_DAYS,
    INTELLECTUAL_CYCLE_DAYS,
)

__all__ = [
    "BiorhythmCalculator",
    "DateValidator",
    "UserInterface",
    "BiorhythmError",
    "DateValidationError",
    "ChartParameterError",
    "main",
    "setup_logging",
    "MIN_YEAR",
    "MAX_YEAR",
    "CRITICAL_DAY_THRESHOLD",
    "PHYSICAL_CYCLE_DAYS",
    "EMOTIONAL_CYCLE_DAYS",
    "INTELLECTUAL_CYCLE_DAYS",
    "__version__",
]

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"
