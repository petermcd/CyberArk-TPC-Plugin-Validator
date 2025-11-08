"""Base class for all section rule sets."""

from collections import Counter

from tpc_plugin_parser.lexer.tokens.assignment import Assignment
from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.rule_set import RuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import Violations


class SectionRuleSet(RuleSet):
    def _validate_duplicates(self) -> None:
        """Validate that the section does not contain duplicate assignments."""
        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        token_keys: list[str] = []
        token_keys.extend(
            token.name.lower()
            for token in section
            if token.token_name
            in (
                TokenName.ASSIGNMENT.value,
                TokenName.CPM_PARAMETER_VALIDATION.value,
            )
        )
        counted_keys = Counter(token_keys)
        for token_lower in counted_keys:
            if counted_keys[token_lower] > 1:
                # TODO - Update so that we can output the line number of the section
                self._add_violation(
                    name=Violations.duplicate_assignment_violation,
                    severity=Severity.CRITICAL,
                    message=f'The assignment "{self.get_first_assignment(token_list=section, token_name=token_lower).name}" has been declared {counted_keys[token_lower]} times.',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                )

    @classmethod
    def get_first_assignment(cls, token_list: list, token_name: str) -> Assignment | None:
        """
        Get the first token in a list with the specified token name.

        :param token_list: List of tokens to search.
        :param token_name: Token name to search for.
        :return: The first token with the specified token name, or None if not found.
        """
        token_name = token_name.lower()

        for token in token_list:
            if token.token_name not in [TokenName.ASSIGNMENT.value, TokenName.CPM_PARAMETER_VALIDATION.value]:
                continue

            if token.name.lower() == token_name:
                return token

        return None
