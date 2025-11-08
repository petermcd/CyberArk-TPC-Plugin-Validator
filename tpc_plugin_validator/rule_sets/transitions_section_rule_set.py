"""Handle validation of the transitions section in the process file."""

import re
from collections import Counter

from tpc_plugin_parser.lexer.tokens.assignment import Assignment
from tpc_plugin_parser.lexer.tokens.transition import Transition
from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.section_rule_set import SectionRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import FileNames, SectionNames, Violations


class TransitionsSectionRuleSet(SectionRuleSet):
    """
    Handle validation of the transitions section in the process file.
    """

    __slots__ = (
        "_default_initial_state",
        "_initial_state",
        "_initial_state_warned",
    )

    _CONFIG_KEY: str = "transitions"
    _FILE_TYPE: FileNames = FileNames.process
    _SECTION_NAME: SectionNames = SectionNames.transitions
    _VALID_TOKENS: list[str] = [
        TokenName.TRANSITION.value,
        TokenName.COMMENT.value,
    ]

    def __init__(self, process_file, prompts_file) -> None:
        """
        Initialize the transitions section rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        """
        self._default_initial_state: str = "Init"
        self._file_sections: str = "init"
        self._initial_state_warned: bool = False
        super().__init__(prompts_file=prompts_file, process_file=process_file)

    def validate(self) -> None:
        """Validate the transitions section of the process file."""
        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        if not section:
            # Missing sections are handled at the file level.
            return

        for transition in section:
            # Set the initial state from the first transition.
            if transition.token_name == TokenName.TRANSITION.value:
                self._initial_state = transition.current_state.lower()
                break

        self._validate_tokens(file=self._FILE_TYPE)
        self._validate_conditions()
        self._validate_duplicates()
        self._validate_states()
        self._validate_state_paths()
        self._validate_transition_reachable()

    def _get_fail_state(self, name: str) -> Assignment | None:
        """
        Fetch a fail state with the given name.

        :param name: The name of the state to fetch.
        :return: The state token or None if the token has not been declared.
        """
        return next(
            (
                state
                for state in self._get_section(file=self._FILE_TYPE, section_name=SectionNames.states)
                if state.token_name == TokenName.FAIL_STATE.value and state.name.lower() == name.lower()
            ),
            None,
        )

    def _validate_conditions(self) -> None:
        """Validate the conditions used in transitions."""
        if not self.has_prompts_file:
            # Skip as we were not supplied the required process file.
            return

        conditions = self._get_section(file=FileNames.prompts, section_name=SectionNames.conditions)
        for transition in self._get_section(file=self._FILE_TYPE, section_name=SectionNames.transitions):
            found = False
            if transition.token_name != TokenName.TRANSITION.value:
                continue
            for condition in conditions:
                if condition.token_name != TokenName.ASSIGNMENT.value:
                    continue
                if transition.condition == condition.name:
                    found = True
                    break
                if transition.condition.lower() == condition.name.lower():
                    found = True
                    self._add_violation(
                        name=Violations.name_case_mismatch_violation,
                        message=f'The condition "{condition.name}" is declared but is used as "{transition.condition}".',
                        severity=Severity.WARNING,
                        file=self._FILE_TYPE,
                        section=self._SECTION_NAME,
                        line=transition.line_number,
                    )
                    break
            if not found:
                self._add_violation(
                    name=Violations.invalid_condition_violation,
                    severity=Severity.CRITICAL,
                    message=f'The condition "{transition.condition}" used in the transition from "{transition.current_state}" to "{transition.next_state}" but has not been declared.',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line=transition.line_number,
                )

    def _validate_duplicates(self) -> None:
        """Check for duplicate state transitions."""
        state_transitions: list[Transition] = []
        state_transitions.extend(
            state_transition
            for state_transition in self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
            if state_transition.token_name == TokenName.TRANSITION.value
        )
        state_transitions_joined: list[str] = []
        state_transitions_joined.extend(
            f"{state_transition.current_state},{state_transition.condition},{state_transition.next_state}".lower()
            for state_transition in state_transitions
        )

        state_transitions_counted = Counter(state_transitions_joined)
        for state in state_transitions_counted:
            if state_transitions_counted[state] > 1:
                # TODO - Update so that we can output the line number of the transition
                self._add_violation(
                    name=Violations.duplicate_transition_violation,
                    severity=Severity.CRITICAL,
                    message=f'The transition "{state}" has been declared {state_transitions_counted[state]} times, a transition triple must be unique.',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line=None,
                )

    def _validate_next_transition(self, transition: Transition, transitions) -> None:
        """
        Check the to_state has a valid transition to start from.

        :param transition: The transitions token to check.
        :param transitions: A list of all the transitions.
        """
        if transition.token_name != TokenName.TRANSITION.value:
            return
        if transition.next_state.lower() == "end":
            return
        from_states: list[str] = []
        from_states.extend(
            value.current_state for value in transitions if value.token_name == TokenName.TRANSITION.value
        )

        if transition.next_state not in from_states:
            fail_state_token: Assignment | None = self._get_fail_state(transition.next_state)
            if fail_state_token and fail_state_token.token_name == TokenName.FAIL_STATE.value:
                # failure condition, nothing follows this.
                return

            self._add_violation(
                name=Violations.invalid_transition_violation,
                severity=Severity.CRITICAL,
                message=f'The state "{transition.current_state}" attempts to transition to "{transition.next_state}" but has not been declared.',
                file=self._FILE_TYPE,
                section=self._SECTION_NAME,
                line=transition.line_number,
            )

    def _validate_previous_transition(self, transition: Transition, transitions) -> None:
        """
        Check the previous token is valid for the transition.

        :param transition: The transition token to check.
        :param transitions: A list of all the transitions.
        """
        if transition.token_name != TokenName.TRANSITION.value:
            return
        if transition.current_state.lower() == self._default_initial_state.lower():
            return
        if transition.current_state.lower() == self._initial_state:
            if self._initial_state_warned:
                return

            self._add_violation(
                name=Violations.name_violation,
                severity=Severity.WARNING,
                message=f'The start state "{transition.current_state}", for clarity should be called "{self._default_initial_state}".',
                file=self._FILE_TYPE,
                section=self._SECTION_NAME,
                line=transition.line_number,
            )
            self._initial_state_warned = True
            return
        to_states: list[str] = []
        to_states.extend(
            value.next_state.lower() for value in transitions if value.token_name == TokenName.TRANSITION.value
        )
        to_states_set = set(to_states)
        if transition.current_state.lower() not in to_states_set:
            self._add_violation(
                name=Violations.invalid_transition_violation,
                severity=Severity.CRITICAL,
                message=f'The state "{transition.current_state}" does not have a valid transition leading to it.',
                file=self._FILE_TYPE,
                section=self._SECTION_NAME,
                line=transition.line_number,
            )

    def _validate_transition_reachable(self):
        """Validate that all states are reachable."""
        bool_conditions: list[str] = []
        if not self.has_prompts_file:
            # Adding presumed bool condition names as we do not have the prompts file to fetch them from.
            bool_conditions.extend(("true", "false"))
            self._add_violation(
                name=Violations.information_only,
                severity=Severity.INFO,
                message=(
                    "The prompts file was not supplied, therefore, assumptions have been made of boolean conditions. "
                    "Transitions that rely on boolean conditions may not validate correctly."
                ),
                file=self._FILE_TYPE,
            )
        else:
            conditions = self._get_section(file=FileNames.prompts, section_name=SectionNames.conditions)
            for condition in conditions:
                # Identify and note and bool conditions declared in the conditions section.
                if condition.token_name != TokenName.ASSIGNMENT.value:
                    continue
                if re.match(r"\(\s*expression\s*\)\s*(true|false)", condition.assigned, re.IGNORECASE):
                    bool_conditions.append(condition.name.lower())
        transition_had_bool: list[str] = []
        for transition in self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME):
            if transition.token_name != TokenName.TRANSITION.value:
                continue
            if transition.current_state.lower() in transition_had_bool:
                # Identify a transitions that comes after a transition that used a boolean condition.
                self._add_violation(
                    name=Violations.unreachable_transition_violation,
                    severity=Severity.CRITICAL,
                    message=f'The transition "{transition.current_state},{transition.condition},{transition.next_state}" is unreachable due to a previous transition from "{transition.current_state}" having a boolean condition.',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line=transition.line_number,
                )
            if transition.condition.lower() in bool_conditions:
                # Add any found transitions that use a boolean condition to the list (must be after checking previous to stop false positives).
                transition_had_bool.append(transition.current_state.lower())

    def _validate_states(self) -> None:
        """Validate that states exist for all transitions and are in the correct case."""
        transitions = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        states = self._get_section(file=self._FILE_TYPE, section_name=SectionNames.states)
        state_names = [
            state.name
            for state in states
            if state.token_name in [TokenName.ASSIGNMENT.value, TokenName.FAIL_STATE.value]
        ]
        state_names_lower = [state.name.lower() for state in states if state.token_name == TokenName.ASSIGNMENT.value]
        for transition in transitions:
            if transition.token_name != TokenName.TRANSITION.value:
                continue

            if transition.current_state not in state_names:
                if transition.current_state.lower() not in state_names_lower:
                    self._add_violation(
                        name=Violations.invalid_transition_violation,
                        severity=Severity.CRITICAL,
                        message=f'The state "{transition.current_state}" used in the transition current state has not been declared.',
                        file=self._FILE_TYPE,
                        section=self._SECTION_NAME,
                        line=transition.line_number,
                    )
                else:
                    state_name = self.get_first_assignment(
                        token_list=states,
                        token_name=transition.current_state,
                    ).name
                    self._add_violation(
                        name=Violations.name_case_mismatch_violation,
                        severity=Severity.WARNING,
                        message=f'The state "{state_name}" is declared but is used with different casing in the transition current state.',
                        file=self._FILE_TYPE,
                        section=self._SECTION_NAME,
                        line=transition.line_number,
                    )
            if transition.next_state not in state_names:
                if transition.next_state.lower() not in state_names_lower:
                    self._add_violation(
                        name=Violations.invalid_transition_violation,
                        severity=Severity.CRITICAL,
                        message=f'The state "{transition.next_state}" used in the transition next state has not been declared.',
                        file=self._FILE_TYPE,
                        section=self._SECTION_NAME,
                        line=transition.line_number,
                    )
                else:
                    state_name = self.get_first_assignment(
                        token_list=states,
                        token_name=transition.next_state,
                    ).name
                    self._add_violation(
                        name=Violations.name_case_mismatch_violation,
                        severity=Severity.WARNING,
                        message=f'The state "{state_name}" is declared but is used with different casing in the transition next state.',
                        file=self._FILE_TYPE,
                        section=self._SECTION_NAME,
                        line=transition.line_number,
                    )

    def _validate_state_paths(self) -> None:
        """Check to ensure that a state has a valid entry and exit point."""
        tokens = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)

        for transition in tokens:
            self._validate_previous_transition(transition=transition, transitions=tokens)
            self._validate_next_transition(transition=transition, transitions=tokens)
