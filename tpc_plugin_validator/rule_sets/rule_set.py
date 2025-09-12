"""Parent class for rule sets."""
from abc import ABC

from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class RuleSet(ABC):
    """Parent class for rule sets."""
    __slots__ = (
        '_config',
        '_process_content',
        '_prompts_content',
        '_violations',
    )


    def __init__(self, process, prompts, config: dict[str, dict[str, bool | int | str]]) -> None:
        """
        Initialize the rule set with prompts and process configurations.

        :param process: Parsed process file.
        :param prompts: Parsed prompts file.
        :param config: Not used, but included for interface consistency.
        """
        self._config = config.get(self.get_config_key(), {})
        self._process_content = process
        self._prompts_content = prompts
        self._violations: list[ValidationResult] = []

    def get_violations(self) -> list[ValidationResult]:
        """
        Getter for the violations.

        :return: List of ValidationResult
        """
        return self._violations

    def _add_violation(self, name: str, description: str, severity: Severity) -> None:
        """
        Add a new violation.

        :param name: The name of the violation.
        :param description: The text describing the violation.
        :param severity: The severity of the violation.
        """
        self._violations.append(
            ValidationResult(
                rule=name,
                message=description,
                severity=severity,
            )
        )

    @staticmethod
    def get_config_key() -> str:
        """
        Property to identify the config key to use for the rule set.

        :return: The config key as a string.
        """
        return 'prompts'
