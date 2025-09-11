import re
from tpc_plugin_validator.utilities.exceptions import LexerException
from tpc_plugin_validator.lexer.tokens.assignment import Assignment
from tpc_plugin_validator.lexer.tokens.comment import Comment
from tpc_plugin_validator.lexer.tokens.eof import EOF
from tpc_plugin_validator.lexer.tokens.fail_state import FailState
from tpc_plugin_validator.lexer.tokens.section_header import SectionHeader
from tpc_plugin_validator.lexer.tokens.state_transition import StateTransition
from tpc_plugin_validator.lexer.utilities.regex import ASSIGNMENT, COMMENT, FAIL_STATE, SECTION_HEADER, TRANSITION
from tpc_plugin_validator.lexer.utilities.token_name import TokenName


class Lexer(object):
    """Object to handle processing the ini files."""

    __slots__ = (
        '_parsed_data',
        '_source',
    )

    def __init__(self, source: str) -> None:
        """Standard init for the Lexer object."""

        self._source = source
        self._parsed_data: list[
            tuple[
                TokenName,
                Assignment | Comment | EOF | FailState | SectionHeader | StateTransition,
            ]
        ] = []

    def process(self):
        """Process the content of the file line by line."""

        if self._parsed_data:
            # Returning as we have parsed the a
            return

        for line in self._source.splitlines():
            if re.match(COMMENT, line):
                self._process_comment(line=line)
                continue
            if re.match(SECTION_HEADER, line):
                self._process_header(line=line)
                continue
            if re.match(TRANSITION, line):
                self._process_state_transition(line=line)
                continue
            if re.match(ASSIGNMENT, line):
                self._process_assignment(line=line)
                continue
            if re.match(FAIL_STATE, line):
                self._process_fail_states(line=line)
                continue
            if not line.strip():
                continue
            raise LexerException(f'Unable to parse: {line}')
        self._parsed_data.append(
            (
                TokenName.EOF,
                EOF(),
            )
        )

    def _process_assignment(self, line: str) -> None:
        """
        Process a variable assignment line

        :param line: Line containing the assignment.
        """
        match = re.match(ASSIGNMENT, line)
        name: str = str(match[1]).strip()
        equals: str | None = str(match[2]).strip() or None
        assigned: str | None = str(match[3]).strip() or None
        self._parsed_data.append((TokenName.ASSIGNMENT, Assignment(name=name, equals=equals, assigned=assigned)))

    def _process_comment(self, line: str) -> None:
        """
        Process the provided comment.

        :param line: Line containing the comment.
        """
        self._parsed_data.append((TokenName.COMMENT, Comment(content=line.strip())))

    def _process_fail_states(self, line: str) -> None:
        """
        Process the provided fail state .

        :param line: Line containing the fail state.
        """
        match = re.match(FAIL_STATE, line)
        self._parsed_data.append(
            (
                TokenName.FAIL_STATE,
                FailState(
                    message=str(match[1]).strip(),
                    code=int(match[2]),
                )
            )
        )

    def _process_header(self, line: str) -> None:
        """
        Process the provided section header.

        :param line: Line containing the section header.
        """
        match = re.match(SECTION_HEADER, line)
        self._parsed_data.append((TokenName.SECTION_HEADER, SectionHeader(name=str(match[1]))))

    def _process_state_transition(self, line: str) -> None:
        """
        Process the provided state transition.

        :param line: Line containing the state transition.
        """
        match = re.match(TRANSITION, line)
        self._parsed_data.append(
            (
                TokenName.STATE_TRANSITION,
                StateTransition(
                    from_state=str(match[1]),
                    condition=str(match[2]),
                    to_state=str(match[3]),
                )
            )
        )
