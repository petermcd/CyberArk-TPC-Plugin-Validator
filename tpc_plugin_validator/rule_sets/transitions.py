"""Handle validation of state transitions."""
from collections import Counter

from tpc_plugin_validator.lexer.tokens.assignment import Assignment
from tpc_plugin_validator.lexer.tokens.state_transition import StateTransition
from tpc_plugin_validator.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.rule_set import RuleSet
from tpc_plugin_validator.utilities.severity import Severity


class Transitions(RuleSet):
    """Handle validation of state transitions."""

    CONFIG_KEY: str = 'transitions'
    SECTION_NAME: str = 'transitions'
    VALID_TOKEN_TYPES: set[str] = {TokenName.COMMENT.value, TokenName.STATE_TRANSITION.value, }

    def validate(self) -> None:
        """Validate the transitions section."""
        if not self._check_section_exists(file_content=self._process_content):
            self._add_violation(
                name='TransitionNoSectionViolation',
                description=f'The process file does not contain a "{self.SECTION_NAME}" section.',
                severity=Severity.CRITICAL,
            )
            return

        state_transitions = self._process_content.get(self._found_section_name, [])
        for state_transition in state_transitions:
            if not self._token_is_valid(token=state_transition):
                self._add_violation(
                    name='TransitionsTokenViolation',
                    description=f'The token type "{state_transition.token_name}" is not valid in the "{self.SECTION_NAME}" section, found on line {state_transition.line_number}.',
                    severity=Severity.WARNING,
                )

        self._check_duplicate_transitions()
        self._check_state_paths_valid()

    def _check_duplicate_transitions(self) -> None:
        """Check for duplicate state transitions."""
        state_transitions: list[StateTransition] = []
        state_transitions.extend(
            state_transition
            for state_transition in self._process_content.get(self._found_section_name, [])
            if state_transition.token_name == TokenName.STATE_TRANSITION.value
        )
        state_transitions_joined: list[str] = []
        state_transitions_joined.extend(
            f'{state_transition.current_state},{state_transition.condition},{state_transition.next_state}'
            for state_transition in state_transitions
        )

        state_transitions_counted = Counter(state_transitions_joined)
        for state in state_transitions_counted:
            if state_transitions_counted[state] > 1:
                self._add_violation(
                    name='TransitionsStateTransitionReuseViolation',
                    description=f'The state transition "{state}" has been declared {state_transitions_counted[state]} times, a state transition should be unique.',
                    severity=Severity.WARNING,
                )

    def _check_state_paths_valid(self):
        """Check to ensure that a state has a valid entry and exit point."""
        tokens = self._process_content.get(self._found_section_name, [])

        for transition in tokens:
            self._check_previous_transition(transition=transition, transitions=tokens)
            self._check_next_transition(transition=transition, transitions=tokens)

    def _check_next_transition(self, transition: StateTransition, transitions) -> None:
        """
        Check the to_state has a valid transition to start from.

        :param transition: The transitions token to check.
        :param transitions: A list of all the transitions.
        """
        if transition.token_name != TokenName.STATE_TRANSITION.value:
            return
        if transition.next_state.lower() == 'end':
            return
        from_states: list[str] = []
        from_states.extend(
            value.current_state
            for value in transitions
            if value.token_name == TokenName.STATE_TRANSITION.value
        )
        if transition.next_state not in from_states:
            fail_state_token: Assignment | None = self._get_fail_state(transition.next_state)
            if fail_state_token and fail_state_token.token_name == TokenName.FAIL_STATE.value:
                # failure condition, nothing follows this.
                return
            self._add_violation(
                name='TransitionsStateTransitionViolation',
                description=f'The state "{transition.next_state}" does not have a valid state to transition too.',
                severity=Severity.WARNING,
            )

    def _check_previous_transition(self, transition: StateTransition, transitions) -> None:
        """
        Check the previous token is valid for the transition.

        :param transition: The transitions token to check.
        :param transitions: A list of all the transitions.
        """
        if transition.token_name != TokenName.STATE_TRANSITION.value:
            return
        if transition.current_state.lower() == 'init':
            return
        to_states: list[str] = []
        to_states.extend(
            value.next_state
            for value in transitions
            if value.token_name == TokenName.STATE_TRANSITION.value
        )
        to_states_set = set(to_states)
        if transition.current_state not in to_states_set:
            self._add_violation(
                name='TransitionsStateTransitionViolation',
                description=f'The state "{transition.current_state}" does not have a valid state to transition from.',
                severity=Severity.WARNING,
            )

    def _get_fail_state(self, name: str) -> Assignment | None:
        """
        Fetch a fail state with the given name.

        :param name: The name of the state to fetch.
        :return: The state token or None if the token does not exist.
        """
        return next(
            (
                state
                for state in self._process_content.get('states', [])
                if state.token_name == TokenName.FAIL_STATE.value and state.name.lower() == name.lower()
            ),
            None,
        )