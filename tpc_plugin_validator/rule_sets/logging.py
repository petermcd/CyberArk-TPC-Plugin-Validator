# Handle validation of the logging settings in the process file.
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class Logging:
    """ Validate the logging settings in the process file. """
    __slots__ = (
        '_enabled',
        '_process_content',
        '_validation_results',
    )

    def __init__(self, process, prompts, config: dict[str, bool | int | str]) -> None:
        """
        Initialize the LoggingValidation with prompts and process configurations.

        :param process: Parsed process file.
        :param prompts: Not used, but included for interface consistency.
        :param config: Dictionary containing setting for enabled with either True for enabled or False for disabled.
        """
        _ = prompts
        self._enabled = config.get('enabled', True)
        self._process_content = process
        self._validation_results: list[ValidationResult] = []

    def validate(self) -> list[ValidationResult]:
        """
        Validate the logging settings in the process file.

        :return: List of ValidationResult objects indicating any issues found.
        """
        if 'Debug Information' not in self._process_content.keys():
            self._validation_results.append(
                ValidationResult(
                    rule='LoggingNoSection',
                    message='The process file does not contain a "Debug Information" section, therefore, logging is disabled.',
                    severity=Severity.INFO,
                )
            )
            return self._validation_results
        logging_tokens = self._process_content['Debug Information']
        for logging_token in logging_tokens:
            if not self._token_is_valid(token=logging_token):
                self._validation_results.append(
                    ValidationResult(
                        rule='LoggingTokenViolation',
                        message=f'The token type "{logging_token.token_name}" is not valid in the "Debug Information" section, found on line {logging_token.line_number}.',
                        severity=Severity.WARNING,
                    )
                )
                continue
            if logging_token.token_name == 'Comment':
                continue
            if not self._check_setting_name(setting=logging_token.name):
                continue
            self._check_setting_value(setting=logging_token.name, value=logging_token.assigned)

        return self._validation_results

    @staticmethod
    def _token_is_valid(token) -> bool:
        """
        Check to ensure that the given token is valid for this section.

        :param token: The token to check.

        :return: True if valid, Otherwise False.
        """
        valid_tokens = ['Assignment', 'Comment']
        return token.token_name in valid_tokens


    def _check_setting_name(self, setting: str) -> bool:
        """
        Check the setting name is valid.

        :param setting: The name of the logging setting.

        :return: True if the setting name is valid, False otherwise.
        """
        valid_settings = [
            'DebugLogFullParsingInfo',
            'DebugLogFullExecutionInfo',
            'DebugLogDetailBuiltInActions',
            'ExpectLog',
            'ConsoleOutput',
        ]
        # TODO check if the name of the setting is in the wrong case.
        if setting not in valid_settings:
            self._validation_results.append(
                ValidationResult(
                    rule='LoggingSettingNameViolation',
                    message=f'The logging setting "{setting}" is not a valid logging setting. Valid settings are: {", ".join(valid_settings)}.',
                    severity=Severity.WARNING,
                )
            )
            return False
        return True

    def _check_setting_value(self, setting: str, value: str) -> None:
        """
        Check the value is in the correct case, is a valid value and is set to no if enabled.

        :param setting: The name of the logging setting.
        :param value: The value of the logging setting.
        """

        if value.lower() not in ['yes', 'no']:
            self._validation_results.append(
                ValidationResult(
                    rule='LoggingValueViolation',
                    message=f'The logging value for "{setting}" is set to "{value}" and is invalid. Valid values are "no" and "yes".',
                    severity=Severity.CRITICAL,
                )
            )
            return

        if value.lower() != value:
            self._validation_results.append(
                ValidationResult(
                    rule='LoggingValueCaseViolation',
                    message=f'The logging value for "{setting}" is set to "{value}" and is not in lower case. Ensure all logging settings are in lower case.',
                    severity=Severity.WARNING,
                )
            )

        if value.lower() != 'no':
            self._validation_results.append(
                ValidationResult(
                    rule='LoggingEnabledViolation',
                    message=f'The logging value for "{setting}" is set to "{value}". It is recommended to set all logging settings to "no" for production environments.',
                    severity=Severity.CRITICAL if self._enabled else Severity.INFO,
                )
            )
