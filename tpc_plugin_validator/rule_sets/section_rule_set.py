"""Base class for all section rule sets."""

from collections import Counter

from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.rule_set import RuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import CONFIG_TYPE, Violations


class SectionRuleSet(RuleSet):
    def __init__(self, process_file, prompts_file, config: CONFIG_TYPE) -> None:
        """
        Initialize the section rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        :param config: Configuration.
        """
        super().__init__(
            prompts_file=prompts_file,
            process_file=process_file,
            config=config,
        )

    def _validate_duplicates(self) -> None:
        """Validate that the section does not contain duplicate assignments."""
        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        token_keys: list[str] = []
        token_keys.extend(
            token.name
            for token in section
            if token.token_name in (TokenName.ASSIGNMENT.value, TokenName.CPM_PARAMETER_VALIDATION.value)
        )
        counted_keys = Counter(token_keys)
        for token_name in counted_keys:
            if counted_keys[token_name] > 1:
                # TODO - Update so that we can output the line number of the section
                self._add_violation(
                    name=Violations.duplicate_assignment_violation,
                    severity=Severity.CRITICAL,
                    message=f'The assignment "{token_name}" has been declared {counted_keys[token_name]} times.',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                )
