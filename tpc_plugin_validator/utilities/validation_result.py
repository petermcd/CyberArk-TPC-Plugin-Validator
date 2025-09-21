"""Class to hold the result of a validation check."""

from dataclasses import dataclass

from tpc_plugin_validator.utilities.severity import Severity


@dataclass
class ValidationResult(object):
    """Class to hold the result of a validation check."""

    rule: str
    severity: Severity
    message: str
