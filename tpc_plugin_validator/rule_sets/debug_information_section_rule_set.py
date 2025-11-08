"""Handle validation of the Debug Information section in the process file."""

from tpc_plugin_parser.lexer.tokens.assignment import Assignment
from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.section_rule_set import SectionRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import FileNames, SectionNames, Violations


class DebugInformationSectionRuleSet(SectionRuleSet):
    """
    Handle validation of the Debug Information section in the process file.
    """

    _CONFIG_KEY: str = "debug_information"
    _FILE_TYPE: FileNames = FileNames.process
    _SECTION_NAME: SectionNames = SectionNames.debug_information
    _VALID_TOKENS: list[str] = [
        TokenName.ASSIGNMENT.value,
        TokenName.COMMENT.value,
    ]

    def __init__(self, process_file, prompts_file) -> None:
        """
        Initialize the Debug Information section rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        """
        super().__init__(prompts_file=prompts_file, process_file=process_file)

    def validate(self) -> None:
        """Validate the Debug Information section of the process file."""
        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        if not section:
            # Missing sections are handled at the file level.
            return

        self._validate_tokens(file=self._FILE_TYPE)

        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)

        for token in section:
            if token.token_name == TokenName.ASSIGNMENT.value and self._check_setting_name(token=token):
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
                self._add_violation(
                    name=Violations.name_case_violation,
                    severity=Severity.WARNING,
                    message=f'The setting "{token.name}" should be set as "{valid_setting}".',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line=token.line_number,
                )
                return True

        self._add_violation(
            name=Violations.name_violation,
            severity=Severity.WARNING,
            message=f'The setting "{token.name}" is not a valid setting. Valid settings are: {", ".join(valid_settings)}.',
            file=self._FILE_TYPE,
            section=self._SECTION_NAME,
            line=token.line_number,
        )
        return False

    def _check_setting_value(self, token: Assignment) -> None:
        """
        Check the value is in the correct case, is a valid value and is set to no if enabled.

        :param token: The setting token.
        """
        valid_values = ["yes", "no"]

        if not token.assigned:
            self._add_violation(
                name=Violations.value_violation,
                severity=Severity.WARNING,
                message=f'The value for "{token.name}" is blank. Setting should be explicitly set to "no".',
                file=self._FILE_TYPE,
                section=self._SECTION_NAME,
                line=token.line_number,
            )
            return

        if token.assigned.lower() not in valid_values:
            self._add_violation(
                name=Violations.value_violation,
                severity=Severity.CRITICAL,
                message=f'The value for "{token.name}" is set to "{token.assigned}" and is invalid. Valid values are "no" and "yes".',
                file=self._FILE_TYPE,
                section=self._SECTION_NAME,
                line=token.line_number,
            )
            return

        if token.assigned.lower() != token.assigned:
            self._add_violation(
                name=Violations.value_case_violation,
                severity=Severity.WARNING,
                message=f'The value for "{token.name}" is set to "{token.assigned}" this should be in lower case.',
                file=self._FILE_TYPE,
                section=self._SECTION_NAME,
                line=token.line_number,
            )

        if token.assigned.lower() != "no":
            self._add_violation(
                name=Violations.logging_enabled_violation,
                severity=Severity.CRITICAL,
                message=f'The value for "{token.name}" is set to "{token.assigned}". It is recommended to set all settings in this section to "no" for production environments.',
                file=self._FILE_TYPE,
                section=self._SECTION_NAME,
                line=token.line_number,
            )
