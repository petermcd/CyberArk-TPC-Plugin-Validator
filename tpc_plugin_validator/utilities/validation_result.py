"""Class to hold the result of a validation check."""

from dataclasses import dataclass

from tpc_plugin_validator.utilities.severity import Severity


@dataclass
class ValidationResult(object):
    """Class to hold the result of a validation check."""

    rule: str
    severity: Severity
    message: str
    file: str | None = None
    section: str | None = None
    line: int | None = None

    def __str__(self):
        """String representation of the validation result."""
        output_message: str = f"{self.severity}: ({self.rule}) {self.message}"
        if self.file is not None:
            output_message += f", file: {self.file}"
        if self.section is not None:
            output_message += f", section: {self.section}"
        if self.line is not None:
            output_message += f", line: {self.line}"
        if any([self.file, self.section, self.line]):
            output_message += "."
        return output_message
