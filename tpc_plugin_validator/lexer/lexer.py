import re

from tpc_plugin_validator.lexer.tokens.assignment import Assignment
from tpc_plugin_validator.lexer.tokens.comment import Comment
from tpc_plugin_validator.lexer.tokens.fail_state import FailState
from tpc_plugin_validator.lexer.tokens.parameter_validation import \
    ParameterValidation
from tpc_plugin_validator.lexer.tokens.section_header import SectionHeader
from tpc_plugin_validator.lexer.tokens.state_transition import StateTransition
from tpc_plugin_validator.lexer.utilities.regex import (ASSIGNMENT, COMMENT,
                                                        FAIL_STATE,
                                                        PARAMETER_VALIDATION,
                                                        SECTION_HEADER,
                                                        TRANSITION)
from tpc_plugin_validator.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.utilities.exceptions import LexerException


class Lexer(object):
    """Object to handle processing the ini files."""

    __slots__ = (
        '_parsed_data',
        '_source',
        '_token_specs',
    )

    def __init__(self, source: str) -> None:
        """Standard init for the Lexer object."""

        self._parsed_data: list[
            tuple[
                TokenName,
                Assignment | Comment | FailState | ParameterValidation | SectionHeader | StateTransition,
            ]
        ] = []
        self._source = source
        self._token_specs = [
            (re.compile(ASSIGNMENT, re.IGNORECASE), TokenName.ASSIGNMENT, '_process_assignment'),
            (re.compile(COMMENT, re.IGNORECASE), TokenName.COMMENT, '_process_comment'),
            (re.compile(FAIL_STATE, re.IGNORECASE), TokenName.FAIL_STATE, '_process_fail_state'),
            (re.compile(PARAMETER_VALIDATION, re.IGNORECASE), TokenName.PARAMETER_VALIDATION, '_process_parameter_validation'),
            (re.compile(SECTION_HEADER, re.IGNORECASE), TokenName.SECTION_HEADER, '_process_section_header'),
            (re.compile(TRANSITION, re.IGNORECASE), TokenName.STATE_TRANSITION, '_process_state_transition'),
        ]

    def process(self):
        """Process the content of the file line by line."""

        if self._parsed_data:
            # Returning as we have parsed the data already.
            return

        for line_number, line in enumerate(self._source.splitlines(), start=1):
            for pattern, _, handler_name in self._token_specs:
                if match := pattern.match(line):
                    getattr(self, handler_name)(match=match, line_number=line_number)
                    break
            else:
                if line.strip():
                    raise LexerException(f'Unable to parse "{line}" on line {line_number}')

    def _process_assignment(self, match: re.Match, line_number: int) -> None:
        """
        Process a variable assignment line

        :param match: Regex match of the assignment.
        """
        name: str = str(match[1]).strip()
        equals = str(match[2]).strip() if match[2] else None
        assigned_stripped = str(match[3]).strip() if match[3] else None
        assigned = assigned_stripped or None
        self._parsed_data.append(
            (
                TokenName.ASSIGNMENT,
                Assignment(
                    name=name,
                    equals=equals,
                    assigned=assigned,
                    line_number=line_number,
                )
            )
        )

    def _process_comment(self, match: re.Match, line_number: int) -> None:
        """
        Process the provided comment.

        :param match: Regex match of the comment.
        """
        self._parsed_data.append(
            (
                TokenName.COMMENT,
                Comment(
                    content=str(match[1]).strip(),
                    line_number=line_number,
                )
            )
        )

    def _process_fail_state(self, match: re.Match, line_number: int) -> None:
        """
        Process the provided fail state .

        :param match: Regex match of the fail state.
        """
        self._parsed_data.append(
            (
                TokenName.FAIL_STATE,
                FailState(
                    message=str(match[1]).strip(),
                    code=int(match[2]),
                    line_number=line_number,
                )
            )
        )

    def _process_section_header(self, match: re.Match, line_number: int) -> None:
        """
        Process the provided section header.

        :param match: Regex match of the section header.
        """
        self._parsed_data.append(
            (
                TokenName.SECTION_HEADER,
                SectionHeader(
                    name=str(match[1]),
                    line_number=line_number,
                )
            )
        )

    def _process_state_transition(self, match: re.Match, line_number: int) -> None:
        """
        Process the provided state transition.

        :param match: Regex match of the state transition.
        """
        self._parsed_data.append(
            (
                TokenName.STATE_TRANSITION,
                StateTransition(
                    from_state=str(match[1]),
                    condition=str(match[2]),
                    to_state=str(match[3]),
                    line_number=line_number,
                )
            )
        )

    def _process_parameter_validation(self, match: re.Match, line_number: int) -> None:
        """
        Process the provided parameter validation.

        :param match: Regex match of the parameter validation.
        """
        allow_characters: str | None = None
        if match['allowcharacters']:
            allow_characters = str(match['allowcharacters']).strip()

        self._parsed_data.append(
            (
                TokenName.PARAMETER_VALIDATION,
                ParameterValidation(
                    name=str(match['name']),
                    source=str(match['source']),
                    mandatory=str(match['mandatory']),
                    allow_characters=allow_characters,
                    line_number=line_number,
                )
            )
        )

    @property
    def tokens(self) -> list[tuple[TokenName, Assignment | Comment | FailState | ParameterValidation | SectionHeader | StateTransition]]:
        """A list of tokens found by the lexer."""
        if not self._parsed_data:
            self.process()
        return self._parsed_data
