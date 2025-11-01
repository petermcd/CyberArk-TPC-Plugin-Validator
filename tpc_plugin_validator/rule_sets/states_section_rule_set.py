"""Handle validation of the states section in the process file."""

from collections import Counter

from tpc_plugin_parser.lexer.tokens.assignment import Assignment
from tpc_plugin_parser.lexer.tokens.fail_state import FailState
from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.section_rule_set import SectionRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import CONFIG_TYPE, FileNames, SectionNames, Violations


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

    def __init__(self, process_file, prompts_file, config: CONFIG_TYPE) -> None:
        """
        Initialize the states section rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        :param config: Configuration.
        """
        super().__init__(prompts_file=prompts_file, process_file=process_file, config=config)

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
        codes: list[int] = []
        lower_limit: int = 1000
        upper_limit: int = 9999
        for fail_state in fail_states:
            codes.append(fail_state.code)
            if fail_state.code < lower_limit or fail_state.code > upper_limit:
                self._add_violation(
                    name=Violations.value_violation,
                    severity=Severity.CRITICAL,
                    message=f'The fail state "{fail_state.name}" has an invalid failure code of "{fail_state.code}", the failure code should be between {lower_limit} and {upper_limit}.',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line=fail_state.line_number,
                )

        counted_codes = Counter(codes)
        for code in counted_codes:
            if counted_codes[code] > 1:
                # TODO - Update so that we can output the line number of the fail state
                self._add_violation(
                    name=Violations.value_violation,
                    severity=Severity.WARNING,
                    message=f'The code "{code}" has been assigned to {counted_codes[code]} different failure states.',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                )

    def _validate_fail_states(self) -> None:
        """Check fail states."""
        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        fail_states: list[FailState] = []
        fail_states.extend(token for token in section if token.token_name == TokenName.FAIL_STATE.value)
        self._validate_fail_state_codes(fail_states=fail_states)

    def _validate_state_utilisation(self):
        """Validate states are utilised."""
        states = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        transition_section = self._get_section(file=self._FILE_TYPE, section_name=SectionNames.transitions)
        state_names = [state.name for state in states if state.token_name == TokenName.ASSIGNMENT.value]
        transitions = [
            transition for transition in transition_section if transition.token_name == TokenName.TRANSITION.value
        ]
        for state_name in state_names:
            if state_name.lower() == "end":
                # END state is validated elsewhere.
                continue
            found = False
            for transition in transitions:
                if state_name in [transition.current_state, transition.next_state]:
                    found = True
                    break
            if not found:
                # TODO - Update so that we can output the line number of the state declaration
                self._add_violation(
                    name=Violations.unused_state_violation,
                    severity=Severity.WARNING,
                    message=f'The state "{state_name}" has been declared but is not utilised in the transitions section.',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                )
