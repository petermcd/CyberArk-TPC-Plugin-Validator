"""Handle validation of the Parameters section in the process file."""

import contextlib

from tpc_plugin_parser.lexer.tokens.assignment import Assignment
from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.section_rule_set import SectionRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import CONFIG_TYPE, FileNames, SectionNames, Violations


class ParametersSectionRuleSet(SectionRuleSet):
    """
    Handle validation of the Parameters section in the process file.
    """

    _CONFIG_KEY: str = "parameters"
    _FILE_TYPE: FileNames = FileNames.process
    _SECTION_NAME: SectionNames = SectionNames.parameters
    _VALID_TOKENS: list[str] = [
        TokenName.ASSIGNMENT.value,
        TokenName.COMMENT.value,
    ]

    def __init__(self, process_file, prompts_file, config: CONFIG_TYPE) -> None:
        """
        Initialize the parameters section rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        :param config: Configuration.
        """
        super().__init__(prompts_file=prompts_file, process_file=process_file, config=config)

    def validate(self) -> None:
        """Validate the Parameters section of the process file."""
        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        if not section:
            # Missing sections are handled at the file level.
            return

        self._validate_tokens(file=self._FILE_TYPE)
        self._validate_duplicates()
        self._validate_human_min_max()

    def _validate_human_min_max(self) -> None:
        """Check that the SendHumanMin and SendHumanMax have valid values if set."""

        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)

        human_min: Assignment | None = None
        human_max: Assignment | None = None

        for token in section:
            if token.token_name == TokenName.ASSIGNMENT.value and token.name == "SendHumanMin":
                human_min = token
            elif token.token_name == TokenName.ASSIGNMENT.value and token.name == "SendHumanMax":
                human_max = token

        if not human_min and not human_max:
            return

        with contextlib.suppress(ValueError):
            if (
                human_min
                and human_min.assigned
                and human_max
                and human_max.assigned
                and float(human_min.assigned) > float(human_max.assigned)
            ):
                message: str = self._create_message(
                    message=f'"SendHumanMin" is set to {float(human_min.assigned)} and "SendHumanMax" is set to {float(human_max.assigned)}, "SendHumanMin" cannot be greater than "SendHumanMax"',
                    section=self._SECTION_NAME,
                    file=self._FILE_TYPE,
                    line_number=None,
                )
                self._add_violation(
                    name=Violations.value_violation,
                    description=message,
                    severity=Severity.CRITICAL,
                )

        try:
            if human_min and human_min.assigned and float(human_min.assigned) < 0:
                message = self._create_message(
                    message=f'"SendHumanMin" is set to {float(human_min.assigned)} this cannot be less than 0',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line_number=human_min.line_number,
                )
                self._add_violation(
                    name=Violations.value_violation,
                    severity=Severity.CRITICAL,
                    description=message,
                )
        except ValueError:
            if human_min:
                message = self._create_message(
                    message=f'"SendHumanMin" is set to "{human_min.assigned}", the value must be numerical',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line_number=human_min.line_number,
                )
                self._add_violation(
                    name=Violations.value_violation,
                    severity=Severity.CRITICAL,
                    description=message,
                )

        try:
            if human_max and human_max.assigned and float(human_max.assigned) < 0:
                message = self._create_message(
                    message=f'"SendHumanMax" is set to {float(human_max.assigned)} this cannot be less than 0',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line_number=human_max.line_number,
                )
                self._add_violation(
                    name=Violations.value_violation,
                    severity=Severity.CRITICAL,
                    description=message,
                )
        except ValueError:
            if human_max:
                message = self._create_message(
                    message=f'"SendHumanMax" is set to "{human_max.assigned}", the value must be numerical',
                    section=self._SECTION_NAME,
                    file=self._FILE_TYPE,
                    line_number=human_max.line_number,
                )
                self._add_violation(
                    name=Violations.value_violation,
                    severity=Severity.CRITICAL,
                    description=message,
                )
