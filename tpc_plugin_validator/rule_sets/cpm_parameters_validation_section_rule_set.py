"""Handle validation of the CPM Parameters Validation section in the process file."""

from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.section_rule_set import SectionRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import CONFIG_TYPE, FileNames, SectionNames, Violations


class CPMParametersValidationSectionRuleSet(SectionRuleSet):
    """
    Handle validation of the CPM Parameters Validation section in the process file.
    """

    _CONFIG_KEY: str = "cpm_parameters_validation"
    _FILE_TYPE: FileNames = FileNames.process
    _SECTION_NAME: SectionNames = SectionNames.cpm_parameters_validation
    _VALID_TOKENS: list[str] = [
        TokenName.CPM_PARAMETER_VALIDATION.value,
        TokenName.COMMENT.value,
    ]

    def __init__(self, process_file, prompts_file, config: CONFIG_TYPE) -> None:
        """
        Initialize the CPM Parameters Validation section rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        :param config: Configuration.
        """
        super().__init__(prompts_file=prompts_file, process_file=process_file, config=config)

    def validate(self) -> None:
        """Validate the CPM Parameters Validation section of the process file."""
        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        if not section:
            # Missing sections are handled at the file level.
            return

        self._validate_tokens(file=self._FILE_TYPE)
        self._validate_parameter_usage()
        self._validate_duplicates()

    def _validate_parameter_usage(self) -> None:
        """Check to make sure the parameter is used."""
        allowed_missing_parameters: set[str] = {
            "ProcessFileName",
            "PromptsFileName",
        }

        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        for token in section:
            if token.token_name != TokenName.CPM_PARAMETER_VALIDATION.value:
                continue

            if token.name in allowed_missing_parameters:
                continue

            if self._validate_token_utilised(token=token):
                continue

            message: str = self._create_message(
                message=f'The parameter "{token.name}" has been validated but is not used',
                file=self._FILE_TYPE,
                section=self._SECTION_NAME,
                line_number=token.line_number,
            )
            self._add_violation(
                name=Violations.unused_parameter_violation,
                description=message,
                severity=Severity.WARNING,
            )

    def _validate_token_utilised(self, token) -> bool:
        """
        Validate that the given token is used.

        :param token: The token to search for.

        :return: True if used, otherwise False.
        """

        conditions = self._get_section(file=FileNames.prompts, section_name=SectionNames.conditions)
        if not conditions:
            return False

        for condition in conditions:
            if condition.token_name != TokenName.ASSIGNMENT.value:
                continue
            if condition.assigned and f"<{token.name}>" in condition.assigned:
                return True

        states = self._get_section(file=FileNames.process, section_name=SectionNames.states)
        for state in states:
            if state.token_name != TokenName.ASSIGNMENT.value:
                continue
            if state.assigned and f"<{token.name}>" in state.assigned:
                return True

        return False
