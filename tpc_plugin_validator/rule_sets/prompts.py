# Handle validation of the prompts file.
from collections import Counter

from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class Prompts:
    """ Validate the logging settings in the process file. """
    __slots__ = (
        '_enabled',
        '_process_content',
        '_prompts_content',
        '_validation_results',
    )

    def __init__(self, process, prompts, config: dict[str, bool | int | str]) -> None:
        """
        Initialize Prompts with prompts and process configurations.

        :param process: Parsed process file.
        :param prompts: Parsed prompts file.
        :param config: Not used, but included for interface consistency.
        """
        self._enabled = config.get('enabled', True)
        self._process_content = process
        self._prompts_content = prompts
        self._validation_results: list[ValidationResult] = []

    def validate(self) -> list[ValidationResult]:
        """
        Validate the prompts in the prompts file.

        :return: List of ValidationResult objects indicating any issues found.
        """
        if 'conditions' not in self._prompts_content.keys():
            self._validation_results.append(
                ValidationResult(
                    rule='PromptsNoConditionSectionViolation',
                    message='The prompts file does not contain a "conditions" section, therefore, the plugin cannot transitions between states.',
                    severity=Severity.CRITICAL,
                )
            )
            return self._validation_results
        conditions = self._prompts_content.get('conditions', {})
        for condition in conditions:
            if not self._token_is_valid(token=condition):
                self._validation_results.append(
                    ValidationResult(
                        rule='PromptsConditionTokenViolation',
                        message=f'The token type "{condition.token_name}" is not valid in the "condition" section, found on line {condition.line_number}.',
                        severity=Severity.WARNING,
                    )
                )
                continue
            if condition.token_name == 'Comment':
                continue
            if not self._check_condition_used(token=condition):
                self._validation_results.append(
                    ValidationResult(
                        rule='PromptsUnusedConditionViolation',
                        message=f'The condition "{condition.name}" is declared in the prompts file on line {condition.line_number} but is not used in the process file.',
                        severity=Severity.WARNING,
                    )
                )

        self._check_default()
        self._check_valid_sections()
        self._check_duplicates()
        return self._validation_results

    def _check_condition_used(self, token) -> bool:
        """
        Check to ensure all conditions are used

        :param token: The token to check.

        :return: True if used, Otherwise False.
        """
        return any(
            token.name == transition.condition
            for transition in self._process_content.get(
                'transitions', {}
            )
        )

    def _check_default(self):
        """Check to ensure the default section of the prompt file is blank or only contains comments."""
        for default_item in self._prompts_content.get('default', []):
            if default_item.token_name != 'Comment':
                self._validation_results.append(
                    ValidationResult(
                        rule='PromptsDefaultContentViolation',
                        message=f'A token of type "{default_item.token_name}" has been found in the prompt file outwith a valid section on line {default_item.line_number}.',
                        severity=Severity.WARNING,
                    )
                )

    def _check_duplicates(self):
        """
        Check to ensure all conditions are used

        :param token: The token to check.
        """
        conditions = self._prompts_content.get('conditions', {})
        condition_keys = []
        condition_keys.extend(condition.name for condition in conditions if condition.token_name == 'Assignment')
        counted_keys = Counter(condition_keys)
        for condition_name in counted_keys:
            if counted_keys[condition_name] > 1:
                self._validation_results.append(
                    ValidationResult(
                        rule='PromptsDuplicateConditionViolation',
                        message=f'The condition "{condition_name}" has been declared {counted_keys[condition_name]} times in the process file.',
                        severity=Severity.WARNING,
                    )
                )

    def _check_valid_sections(self):
        """Check to ensure only valid sections are found the prompt file."""
        allowed_sections = ('default', 'conditions')
        for section_name in self._prompts_content.keys():
            if section_name not in allowed_sections:
                self._validation_results.append(
                    ValidationResult(
                        rule='PromptsInvalidSectionViolation',
                        message=f'An invalid section "{section_name}" has been found in the prompt file.',
                        severity=Severity.WARNING,
                    )
                )

    @staticmethod
    def _token_is_valid(token) -> bool:
        """
        Check to ensure that the given token is valid for this section.

        :param token: The token to check.

        :return: True if valid, Otherwise False.
        """
        valid_tokens = ['Assignment', 'Comment']
        return token.token_name in valid_tokens

    @staticmethod
    def get_config_key() -> str:
        """
        Property to identify the config key to use for the rule set.

        :return: The config key as a string.
        """
        return 'prompts'
