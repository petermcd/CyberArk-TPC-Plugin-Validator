"""Handle validation of the conditions section in the process file."""

from tpc_plugin_parser.lexer.tokens.assignment import Assignment
from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.section_rule_set import SectionRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import CONFIG_TYPE, FileNames, SectionNames, Violations


class ConditionsSectionRuleSet(SectionRuleSet):
    """
    Handle validation of the conditions section in the process file.
    """

    _CONFIG_KEY: str = "conditions"
    _FILE_TYPE: FileNames = FileNames.prompts
    _SECTION_NAME: SectionNames = SectionNames.conditions
    _VALID_TOKENS: list[str] = [
        TokenName.ASSIGNMENT.value,
        TokenName.COMMENT.value,
    ]

    def __init__(self, process_file, prompts_file, config: CONFIG_TYPE) -> None:
        """
        Initialize the conditions section rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        :param config: Configuration.
        """
        super().__init__(prompts_file=prompts_file, process_file=process_file, config=config)

    def validate(self) -> None:
        """Validate the conditions section of the prompts file."""
        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        if not section:
            # Missing sections are handled at the file level.
            return

        self._validate_tokens(file=self._FILE_TYPE)
        self._validate_duplicates()
        self._validate_conditions_utilised()

    def _validate_conditions_utilised(self) -> None:
        """Check to ensure all conditions are used and case matches."""
        required_tokens: list[Assignment] = []
        required_tokens.extend(
            token
            for token in self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
            if token.token_name == TokenName.ASSIGNMENT.value
        )
        transitions = self._get_section(file=FileNames.process, section_name=SectionNames.transitions)

        for token in required_tokens:
            found = False
            for transition in transitions:
                if transition.token_name != TokenName.TRANSITION.value:
                    continue
                if token.name == transition.condition:
                    found = True
                    continue
                if token.name.lower() == transition.condition.lower():
                    message: str = self._create_message(
                        message=f'The condition "{token.name}" is declared but is used as "{transition.condition}"',
                        file=self._FILE_TYPE,
                        section=self._SECTION_NAME,
                        line_number=token.line_number,
                    )
                    self._add_violation(
                        name=Violations.name_case_mismatch_violation,
                        description=message,
                        severity=Severity.WARNING,
                    )
                    found = True
                    break
            if found:
                continue
            message = self._create_message(
                message=f'The condition "{token.name}" is declared but is not used',
                file=self._FILE_TYPE,
                section=self._SECTION_NAME,
                line_number=token.line_number,
            )
            self._add_violation(
                name=Violations.unused_condition_violation,
                description=message,
                severity=Severity.WARNING,
            )
