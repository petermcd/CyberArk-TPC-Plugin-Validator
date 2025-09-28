"""Handle validation of the transitions section in the process file."""

from collections import Counter

from tpc_plugin_parser.lexer.tokens.assignment import Assignment
from tpc_plugin_parser.lexer.tokens.transition import Transition
from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.section_rule_set import SectionRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import CONFIG_TYPE, FileNames, SectionNames, Violations


class TransitionsSectionRuleSet(SectionRuleSet):
    """
    Handle validation of the transitions section in the process file.
    """

    _CONFIG_KEY: str = "transitions"
    _FILE_TYPE: FileNames = FileNames.process
    _SECTION_NAME: SectionNames = SectionNames.transitions
    _VALID_TOKENS: list[str] = [
        TokenName.TRANSITION.value,
        TokenName.COMMENT.value,
    ]

    def __init__(self, process_file, prompts_file, config: CONFIG_TYPE) -> None:
        """
        Initialize the transitions section rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        :param config: Configuration.
        """
        super().__init__(prompts_file=prompts_file, process_file=process_file, config=config)

    def validate(self) -> None:
        """Validate the transitions section of the process file."""
        section = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)
        if not section:
            # Missing sections are handled at the file level.
            return

        self._validate_tokens(file=self._FILE_TYPE)
        self._validate_duplicates()
        self._validate_state_paths()

    def _get_fail_state(self, name: str) -> Assignment | None:
        """
        Fetch a fail state with the given name.

        :param name: The name of the state to fetch.
        :return: The state token or None if the token does not exist.
        """
        return next(
            (
                state
                for state in self._get_section(file=self._FILE_TYPE, section_name=SectionNames.states)
                if state.token_name == TokenName.FAIL_STATE.value and state.name.lower() == name.lower()
            ),
            None,
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
            f"{state_transition.current_state},{state_transition.condition},{state_transition.next_state}"
            for state_transition in state_transitions
        )

        state_transitions_counted = Counter(state_transitions_joined)
        for state in state_transitions_counted:
            if state_transitions_counted[state] > 1:
                message: str = self._create_message(
                    message=f'The transition "{state}" has been declared {state_transitions_counted[state]} times, a transition tuple must be unique',
                    file=self._FILE_TYPE,
                    section=self._SECTION_NAME,
                    line_number=None,
                )
                self._add_violation(
                    name=Violations.duplicate_transition_violation,
                    description=message,
                    severity=Severity.WARNING,
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
            message: str = self._create_message(
                message=f'The state "{transition.current_state}" attempts to transition to "{transition.next_state}" which does not exist',
                file=self._FILE_TYPE,
                section=self._SECTION_NAME,
                line_number=transition.line_number,
            )
            self._add_violation(
                name=Violations.invalid_transition_violation,
                description=message,
                severity=Severity.CRITICAL,
            )

    def _validate_previous_transition(self, transition: Transition, transitions) -> None:
        """
        Check the previous token is valid for the transition.

        :param transition: The transitions token to check.
        :param transitions: A list of all the transitions.
        """
        if transition.token_name != TokenName.TRANSITION.value:
            return
        if transition.current_state.lower() == "init":
            return
        to_states: list[str] = []
        to_states.extend(value.next_state for value in transitions if value.token_name == TokenName.TRANSITION.value)
        to_states_set = set(to_states)
        if transition.current_state not in to_states_set:
            message: str = self._create_message(
                message=f'The state "{transition.current_state}" does not have a valid path leading to it',
                file=self._FILE_TYPE,
                section=self._SECTION_NAME,
                line_number=transition.line_number,
            )
            self._add_violation(
                name=Violations.invalid_transition_violation,
                description=message,
                severity=Severity.CRITICAL,
            )

    def _validate_state_paths(self) -> None:
        """Check to ensure that a state has a valid entry and exit point."""
        tokens = self._get_section(file=self._FILE_TYPE, section_name=self._SECTION_NAME)

        for transition in tokens:
            self._validate_previous_transition(transition=transition, transitions=tokens)
            self._validate_next_transition(transition=transition, transitions=tokens)
