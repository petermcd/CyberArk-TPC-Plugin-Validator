"""Handle validation of states."""
from collections import Counter

from tpc_plugin_validator.lexer.tokens.assignment import Assignment
from tpc_plugin_validator.lexer.tokens.fail_state import FailState
from tpc_plugin_validator.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.rule_set import RuleSet
from tpc_plugin_validator.utilities.severity import Severity


class States(RuleSet):
    """Handle validation of states."""

    CONFIG_KEY: str = 'states'
    SECTION_NAME = 'states'
    VALID_TOKEN_TYPES: set[str] = {TokenName.ASSIGNMENT.value, TokenName.COMMENT.value, TokenName.FAIL_STATE.value, }

    def validate(self) -> None:
        """Validate the states in the process file."""
        if not self._check_section_exists(file_content=self._process_content):
            self._add_violation(
                name='StatesNoStatesSectionViolation',
                description=f'The process file does not contain a "{self.SECTION_NAME}" section.',
                severity=Severity.CRITICAL,
            )
            return

        states = self._process_content.get(self._found_section_name, [])
        for state in states:
            if not self._token_is_valid(token=state):
                self._add_violation(
                    name='StatesTokenViolation',
                    description=f'The token type "{state.token_name}" is not valid in the "{self.SECTION_NAME}" section, found on line {state.line_number}.',
                    severity=Severity.WARNING,
                )

        self._check_duplicates(
            tokens=states,
            rule_name='StatesDuplicateParametersViolation',
            file_type='process'
        )
        self._check_valid_end_state()
        self._check_fail_states()

    def _check_fail_state_codes(self, fail_states: list[FailState]):
        """Check the code is valid for the """
        codes: list[int] = []
        for fail_state in fail_states:
            codes.append(fail_state.code)
            if fail_state.code < 1000 or fail_state.code > 9999:
                self._add_violation(
                    name='StatesFailStateViolation',
                    description=f'A fail state has a failure code of "{fail_state.code}", the failure code should be a 4 digit code, found on line {fail_state.line_number}.',
                    severity=Severity.CRITICAL,
                )

        counted_codes = Counter(codes)
        for code in counted_codes:
            if counted_codes[code] > 1:
                self._add_violation(
                    name='StatesFailStateCodeReuseViolation',
                    description=f'The code "{code}" has been assigned {counted_codes[code]} times in the "{self.SECTION_NAME}" section, codes should not be reused.',
                    severity=Severity.WARNING,
                )

    def _check_fail_states(self) -> None:
        """Check fail states."""
        fail_states: list[FailState] = []
        fail_states.extend(
            state
            for state in self._process_content.get(self._found_section_name, [])
            if state.token_name == TokenName.FAIL_STATE.value
        )
        self._check_fail_state_codes(fail_states=fail_states)

    def _check_valid_end_state(self) -> None:
        """Check to ensure that the states contain a valid END state."""
        end_state: Assignment | None = None
        for state in self._process_content.get(self._found_section_name, []):
            if state.token_name == TokenName.ASSIGNMENT.value and state.name == 'END':
                end_state = state
                break
            elif state.token_name == 'Assignment' and state.name.lower() == 'end':
                end_state = state
                self._add_violation(
                    name='StatesEndStateCaseViolation',
                    description=f'The END state has been declared as "{end_state.name}", the END state should be in upper case, found on line {end_state.line_number}.',
                    severity=Severity.CRITICAL,
                )
                break
        if end_state and end_state.assigned is not None:
            self._add_violation(
                name='StatesEndStateValueViolation',
                description=f'The END state has been assigned the value "{end_state.assigned}", the END state should not have a value, found on line {end_state.line_number}.',
                severity=Severity.CRITICAL,
            )
