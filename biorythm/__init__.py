"""
Biorythm calculation library.

A Python library for generating biorhythm charts and timeseries data 
based on the pseudoscientific biorhythm theory.

WARNING: This software implements biorhythm theory, which is considered 
PSEUDOSCIENCE. This implementation is provided FOR ENTERTAINMENT PURPOSES ONLY.
"""

__version__ = "0.1.0"

from .core import (
    BiorhythmCalculator,
    DateValidator,
    UserInterface,
    BiorhythmError,
    DateValidationError,
    main,
    setup_logging,
    MIN_YEAR,
    MAX_YEAR,
    CRITICAL_DAY_THRESHOLD,
)

__all__ = [
    "BiorhythmCalculator",
    "DateValidator", 
    "UserInterface",
    "BiorhythmError",
    "DateValidationError",
    "main",
    "setup_logging",
    "MIN_YEAR",
    "MAX_YEAR", 
    "CRITICAL_DAY_THRESHOLD",
    "__version__",
]