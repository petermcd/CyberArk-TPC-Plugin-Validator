"""Parent class for rule sets."""
from abc import ABC
from collections import Counter

from tpc_plugin_validator.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class RuleSet(ABC):
    """Parent class for rule sets."""

    __slots__ = (
        '_config',
        '_found_section_name',
        '_process_content',
        '_prompts_content',
        '_violations',
    )

    CONFIG_KEY: str = ''
    SECTION_NAME: str = ''
    VALID_TOKEN_TYPES: set[str] = {TokenName.ASSIGNMENT.value, TokenName.COMMENT.value,}

    def __init__(self, process, prompts, config: dict[str, dict[str, bool | int | str]]) -> None:
        """
        Initialize the rule set with prompts and process configurations.

        :param process: Parsed process file.
        :param prompts: Parsed prompts file.
        :param config: Not used, but included for interface consistency.
        """
        self._config = config.get(self.CONFIG_KEY, {})
        self._found_section_name = ''
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

    def _check_duplicates(self, tokens, rule_name: str, file_type: str):
        """
        Check to ensure there are no duplicate assignment tokens.

        :param tokens: A list of tokens.
        :param file_type: The type of file being processed (process, prompts).
        """
        token_keys: list[str] = []
        token_keys.extend(token.name for token in tokens if token.token_name == TokenName.ASSIGNMENT.value)
        counted_keys = Counter(token_keys)
        for token_name in counted_keys:
            if counted_keys[token_name] > 1:
                self._add_violation(
                    name=rule_name,
                    description=f'The assignment "{token_name}" has been declared {counted_keys[token_name]} times in the {file_type} file.',
                    severity=Severity.WARNING,
                )

    def _check_section_exists(self, file_content) -> bool:
        """Check to make sure that a section is named appropriately."""

        section_keys = file_content.keys()
        for section_key in section_keys:
            if self.SECTION_NAME == section_key:
                self._found_section_name = section_key
                return True
            elif self.SECTION_NAME.lower() == section_key.lower():
                self._add_violation(
                    name='SectionCaseMismatchViolation',
                    description=f'The "{self.SECTION_NAME}" section has been declared as "{section_key}".',
                    severity=Severity.WARNING,
                )
                self._found_section_name = section_key
                return True
        return False

    def _token_is_valid(self, token) -> bool:
        """
        Check to ensure that the given token is valid for this section.

        :param token: The token to check.

        :return: True if valid, Otherwise False.
        """
        return token.token_name in self.VALID_TOKEN_TYPES
