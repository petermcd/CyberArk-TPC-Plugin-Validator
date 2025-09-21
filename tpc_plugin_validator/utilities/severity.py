"""Structure to hold severity levels for validation results."""

from enum import Enum


class Severity(Enum):
    """Enum to specify the valid severity levels."""

    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
