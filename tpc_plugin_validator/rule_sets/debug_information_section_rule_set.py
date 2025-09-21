"""Handle validation of the Debug Information section in the process file."""

from tpc_plugin_validator.lexer.tokens.assignment import Assignment
from tpc_plugin_validator.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.rule_set import FileNames
from tpc_plugin_validator.rule_sets.section_rule_set import SectionRuleSet
from tpc_plugin_validator.utilities.severity import Severity


class DebugInformationSectionRuleSet(SectionRuleSet):
    """
    Handle validation of the Debug Information section in the process file.
    """

    _CONFIG_KEY: str = "debug_information"
    _FILE_TYPE: FileNames = FileNames.process
    _SECTION_NAME: str = "Debug Information"
    _VALID_TOKENS: list[str] = [
        TokenName.ASSIGNMENT.value,
        TokenName.COMMENT.value,
    ]

    def __init__(
        self, process_file, prompts_file, config: dict[str, dict[str, bool | int | str]]
    ) -> None:
        """
        Initialize the Debug Information section rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        :param config: Not used, but included for interface consistency.
        """
        super().__init__(
            prompts_file=prompts_file, process_file=process_file, config=config
        )

    def validate(self) -> None:
        """Validate the Debug Information section of the process file."""
        section = self._get_section(
            file=self._FILE_TYPE, section_name=self._SECTION_NAME
        )
        if not section:
            # Missing sections are handled at the file level.
            return

        self._validate_tokens(file=self._FILE_TYPE)

        section = self._get_section(
            file=self._FILE_TYPE, section_name=self._SECTION_NAME
        )

        for token in section:
            if (
                token.token_name == TokenName.ASSIGNMENT.value
                and self._check_setting_name(token=token)
            ):
                self._check_setting_value(token=token)

        self._validate_duplicates()

    def _check_setting_name(self, token: Assignment) -> bool:
        """
        Check the setting name is valid.

        :param token: The token containing the Debug Information setting.

        :return: True if the setting name is valid regardless of case, False otherwise.
        """
        valid_settings = [
            "DebugLogFullParsingInfo",
            "DebugLogFullExecutionInfo",
            "DebugLogDetailBuiltInActions",
            "ExpectLog",
            "ConsoleOutput",
        ]
        if token.name in valid_settings:
            return True
        for valid_setting in valid_settings:
            if token.name.lower() == valid_setting.lower():
                message: str = self._create_message(
                    message=f'The setting "{token.name}" in the "{self._SECTION_NAME}" section should be set as "{valid_setting}"',
                    file=self._FILE_TYPE,
                    line_number=token.line_number,
                )
                self._add_violation(
                    name="NameCaseViolation",
                    description=message,
                    severity=Severity.WARNING,
                )
                return True
        message = self._create_message(
            message=f'The setting "{token.name}" in the "{self._SECTION_NAME}" section is not a valid "{self._SECTION_NAME}" setting. Valid settings are: {", ".join(valid_settings)}',
            file=self._FILE_TYPE,
            line_number=token.line_number,
        )
        self._add_violation(
            name="NameViolation",
            description=message,
            severity=Severity.WARNING,
        )
        return False

    def _check_setting_value(self, token: Assignment) -> None:
        """
        Check the value is in the correct case, is a valid value and is set to no if enabled.

        :param token: The setting token.
        """
        valid_values = ["yes", "no"]

        if not token.assigned:
            message: str = self._create_message(
                message=f'The value for "{token.name}" in the "{self._SECTION_NAME}" section is blank. Setting should be explicitly set to "no"',
                file=self._FILE_TYPE,
                line_number=token.line_number,
            )
            self._add_violation(
                name="ValueViolation",
                description=message,
                severity=Severity.WARNING,
            )
            return

        if token.assigned.lower() not in valid_values:
            message = self._create_message(
                message=f'The value for "{token.name}" in the "{self._SECTION_NAME}" section is set to "{token.assigned}" and is invalid. Valid values are "no" and "yes"',
                file=self._FILE_TYPE,
                line_number=token.line_number,
            )
            self._add_violation(
                name="ValueViolation",
                description=message,
                severity=Severity.CRITICAL,
            )
            return

        if token.assigned.lower() != token.assigned:
            message = self._create_message(
                message=f'The value for "{token.name}" in the "{self._SECTION_NAME}" section is set to "{token.assigned}" this should be in lower case',
                file=self._FILE_TYPE,
                line_number=token.line_number,
            )
            self._add_violation(
                name="ValueCaseViolation",
                description=message,
                severity=Severity.WARNING,
            )

        if token.assigned.lower() != "no":
            message = self._create_message(
                message=f'The value for "{token.name}" in the "{self._SECTION_NAME}" section is set to "{token.assigned}". It is recommended to set all "{self._SECTION_NAME}" settings to "no" for production environments',
                file=self._FILE_TYPE,
                line_number=token.line_number,
            )
            self._add_violation(
                name="LoggingEnabledViolation",
                description=message,
                severity=Severity.CRITICAL
                if self._config.get("enabled", True)
                else Severity.INFO,
            )
