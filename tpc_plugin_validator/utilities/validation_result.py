"""Class to hold the result of a validation check."""

from dataclasses import dataclass

from tpc_plugin_validator.utilities.severity import Severity


@dataclass
class ValidationResult(object):
    """Class to hold the result of a validation check."""

    rule: str
    severity: Severity
    message: str
    file: str = ""
    section: str = ""
    line: int = 0

    def __str__(self):
        """String representation of the validation result."""
        file_details = ""
        if self.file:
            file_details += f" {self.file}"
        if self.section:
            file_details += f":{self.section}"
        if self.line:
            file_details += f"({self.line})"
        output_message: str = f"{self.severity.value} -{file_details} ({self.rule}) {self.message}"
        return output_message
