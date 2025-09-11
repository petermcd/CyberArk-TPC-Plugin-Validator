# Structure to hold severity levels for validation results.

from enum import Enum

class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
