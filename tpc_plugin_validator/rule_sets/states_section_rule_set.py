"""Handle validation of the states section in the process file."""

from collections import Counter

from tpc_plugin_parser.lexer.tokens.assignment import Assignment
from tpc_plugin_parser.lexer.tokens.fail_state import FailState
from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.section_rule_set import SectionRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import FileNames, SectionNames, Violations


class StatesSectionRuleSet(SectionRuleSet):
    """
    Handle validation of the states section in the process file.
    """

    _CONFIG_KEY: str = "states"
    _FILE_TYPE: FileNames = FileNames.process
    _SECTION_NAME: SectionNames = SectionNames.states
    _VALID_TOKENS: list[str] = [
        TokenName.ASSIGNMENT.value,
        TokenName.COMMENT.value,
        TokenName.FAIL_STATE.value,
    ]

    def validate(self) -> None:
        """Validate the states section of the process file."""
        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        if not section:
            # Missing sections are handled at the file level.
            return

        self._validate_tokens(file=self._FILE_TYPE)
        self._validate_state_utilisation()
        self._validate_fail_states()
        self._validate_end_state()
        self._validate_duplicates()

    def _validate_end_state(self) -> None:
        """Validate that the states contain a valid END state."""
        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        end_state: Assignment | None = None
        for token in section:
            if token.token_name == TokenName.ASSIGNMENT.value and token.name == "END":
                end_state = token
                break
            elif token.token_name == "Assignment" and token.name.lower() == "end":
                end_state = token
                self._add_violation(
                    name=Violations.name_case_violation,
                    severity=Severity.CRITICAL,
                    message=f'The "END" state has been declared as "{end_state.name}", the "END" state should be in upper case.',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line=end_state.line_number,
                )
                break
        if end_state and end_state.assigned is not None:
            self._add_violation(
                name=Violations.value_violation,
                severity=Severity.CRITICAL,
                message=f'The "END" state has been assigned the value "{end_state.assigned}", the "END" state should not have a value.',
                file=self._FILE_TYPE,
                section=self._SECTION_NAME,
                line=end_state.line_number,
            )

    def _validate_fail_state_codes(self, fail_states: list[FailState]) -> None:
        """
        Check the code is valid for the fail state.

        :param fail_states: A list of found Fail States.
        """
        codes: dict[int, int] = {}
        lower_limit: int = 1000
        upper_limit: int = 9999
        for fail_state in fail_states:
            codes[fail_state.line_number] = fail_state.code
            if fail_state.code < lower_limit or fail_state.code > upper_limit:
                self._add_violation(
                    name=Violations.value_violation,
                    severity=Severity.CRITICAL,
                    message=f'The fail state "{fail_state.name}" has an invalid failure code of "{fail_state.code}", the failure code should be between {lower_limit} and {upper_limit}.',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line=fail_state.line_number,
                )

        counted_codes = Counter(codes.values() if codes else [])
        for code, value in counted_codes.items():
            if value > 1:
                line = next(
                    (code_line for code_line, value_ in codes.items() if value_ == code),
                    0,
                )
                self._add_violation(
                    name=Violations.value_violation,
                    severity=Severity.WARNING,
                    message=f'The code "{code}" has been assigned to {counted_codes[code]} different failure states.',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line=line,
                )

    def _validate_fail_states(self) -> None:
        """Check fail states."""
        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        fail_states: list[FailState] = []
        fail_states.extend(token for token in section if token.token_name == TokenName.FAIL_STATE.value)
        self._validate_fail_state_codes(fail_states=fail_states)

    def _validate_state_utilisation(self):
        """Validate states are utilised."""
        states_section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        transition_section = self._get_section(file=self._FILE_TYPE, section_name=SectionNames.transitions)
        states = [state for state in states_section if state.token_name == TokenName.ASSIGNMENT.value]
        transitions = [
            transition for transition in transition_section if transition.token_name == TokenName.TRANSITION.value
        ]
        for state in states:
            if state.name.lower() == "end":
                # END state is validated elsewhere.
                continue
            found = any(state.name in [transition.current_state, transition.next_state] for transition in transitions)
            if not found:
                self._add_violation(
                    name=Violations.unused_state_violation,
                    severity=Severity.WARNING,
                    message=f'The state "{state.name}" has been declared but is not utilised in the transitions section.',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line=state.line_number,
                )
