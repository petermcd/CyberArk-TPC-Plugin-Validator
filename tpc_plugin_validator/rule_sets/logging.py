"""Handle validation of the logging settings in the process file."""
from tpc_plugin_validator.lexer.tokens.assignment import Assignment
from tpc_plugin_validator.rule_sets.rule_set import RuleSet
from tpc_plugin_validator.utilities.severity import Severity


class Logging(RuleSet):
    """ Validate the logging settings in the process file. """

    def validate(self) -> None:
        """Validate the logging settings in the process file."""
        if 'Debug Information' not in self._process_content.keys():
            self._add_violation(
                name='LoggingNoSection',
                description='The process file does not contain a "Debug Information" section, therefore, logging is disabled.',
                severity=Severity.INFO,
            )
            return
        logging_tokens = self._process_content['Debug Information']
        for logging_token in logging_tokens:
            if not self._token_is_valid(token=logging_token):
                self._add_violation(
                    name='LoggingTokenViolation',
                    description=f'The token type "{logging_token.token_name}" is not valid in the "Debug Information" section, found on line {logging_token.line_number}.',
                    severity=Severity.WARNING,
                )
                continue
            if logging_token.token_name == 'Comment':
                continue
            if not self._check_setting_name(token=logging_token):
                continue
            self._check_setting_value(token=logging_token)

    def _check_setting_name(self, token: Assignment) -> bool:
        """
        Check the setting name is valid.

        :param token: The token containing the logging setting.

        :return: True if the setting name is valid, False otherwise.
        """
        valid_settings = [
            'DebugLogFullParsingInfo',
            'DebugLogFullExecutionInfo',
            'DebugLogDetailBuiltInActions',
            'ExpectLog',
            'ConsoleOutput',
        ]
        if token.name in valid_settings:
            return True
        for valid_setting in valid_settings:
            if token.name.lower() == valid_setting.lower():
                self._add_violation(
                    name='LoggingSettingNameCaseViolation',
                    description=f'The logging setting "{token.name}" should be set as "{valid_setting}".',
                    severity=Severity.WARNING,
                )
                return False
        self._add_violation(
            name='LoggingSettingNameViolation',
            description=f'The logging setting "{token.name}" is not a valid logging setting. Valid settings are: {", ".join(valid_settings)}.',
            severity=Severity.WARNING,
        )
        return False

    def _check_setting_value(self, token: Assignment) -> None:
        """
        Check the value is in the correct case, is a valid value and is set to no if enabled.

        :param token: The setting token.
        """

        if not token.assigned:
            self._add_violation(
                name='LoggingValueViolation',
                description=f'The logging value for "{token.name}" is blank. Setting should explicitly be set to "no".',
                severity=Severity.WARNING,
            )
            return

        if token.assigned.lower() not in ['yes', 'no']:
            self._add_violation(
                name='LoggingValueViolation',
                description=f'The logging value for "{token.name}" is set to "{token.assigned}" and is invalid. Valid values are "no" and "yes".',
                severity=Severity.CRITICAL,
            )
            return

        if token.assigned.lower() != token.assigned:
            self._add_violation(
                name='LoggingValueCaseViolation',
                description=f'The logging value for "{token.name}" is set to "{token.assigned}" and is not in lower case. Ensure all logging settings are in lower case.',
                severity=Severity.WARNING,
            )

        if token.assigned.lower() != 'no':
            self._add_violation(
                name='LoggingEnabledViolation',
                description=f'The logging value for "{token.name}" is set to "{token.assigned}". It is recommended to set all logging settings to "no" for production environments.',
                severity=Severity.CRITICAL if self._config.get('enabled', True) else Severity.INFO,
            )

    def _get_config_key(self) -> str:
        """
        Property to identify the config key to use for the rule set.

        :return: The config key as a string.
        """
        return 'logging'

    def _get_valid_token_types(self) -> set[str]:
        """
        Provide a set of token types allowed in the section being analysed.

        :return: Set of token types.
        """
        return {'Assignment', 'Comment',}
