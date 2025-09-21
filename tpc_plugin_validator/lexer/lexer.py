import re

from tpc_plugin_validator.lexer.tokens.assignment import Assignment
from tpc_plugin_validator.lexer.tokens.comment import Comment
from tpc_plugin_validator.lexer.tokens.cpm_parameter_validation import (
    CPMParameterValidation,
)
from tpc_plugin_validator.lexer.tokens.fail_state import FailState
from tpc_plugin_validator.lexer.tokens.section_header import SectionHeader
from tpc_plugin_validator.lexer.tokens.transition import Transition
from tpc_plugin_validator.lexer.utilities.regex import (
    ASSIGNMENT,
    COMMENT,
    CPM_PARAMETER_VALIDATION,
    FAIL_STATE,
    SECTION_HEADER,
    TRANSITION,
)
from tpc_plugin_validator.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.lexer.utilities.types import ALL_TOKEN_TYPES, TokenSpecs
from tpc_plugin_validator.utilities.exceptions import LexerException


class Lexer(object):
    """Object to handle processing the ini files."""

    __slots__ = (
        "_parsed_data",
        "_source",
        "_token_specs",
    )

    def __init__(self, source: str) -> None:
        """Standard init for the Lexer object."""

        self._parsed_data: list[
            tuple[
                TokenName,
                ALL_TOKEN_TYPES,
            ]
        ] = []
        self._source: str = source
        self._token_specs: list[TokenSpecs] = [
            {
                "pattern": re.compile(ASSIGNMENT, re.IGNORECASE),
                "token_name": TokenName.ASSIGNMENT,
                "processor_method": "_process_assignment",
            },
            {
                "pattern": re.compile(COMMENT, re.IGNORECASE),
                "token_name": TokenName.COMMENT,
                "processor_method": "_process_comment",
            },
            {
                "pattern": re.compile(CPM_PARAMETER_VALIDATION, re.IGNORECASE),
                "token_name": TokenName.CPM_PARAMETER_VALIDATION,
                "processor_method": "_process_cpm_parameter_validation",
            },
            {
                "pattern": re.compile(FAIL_STATE, re.IGNORECASE),
                "token_name": TokenName.FAIL_STATE,
                "processor_method": "_process_fail_state",
            },
            {
                "pattern": re.compile(SECTION_HEADER, re.IGNORECASE),
                "token_name": TokenName.SECTION_HEADER,
                "processor_method": "_process_section_header",
            },
            {
                "pattern": re.compile(TRANSITION, re.IGNORECASE),
                "token_name": TokenName.TRANSITION,
                "processor_method": "_process_transitions",
            },
        ]

    def process(self) -> None:
        """
        Process the content of the file line by line.

        :raises LexerException: If the line is not valid.
        """

        if self._parsed_data:
            # Returning as we have parsed the data already.
            return

        for line_number, line in enumerate(self._source.splitlines(), start=1):
            for token_spec in self._token_specs:
                if match := token_spec["pattern"].match(line):
                    getattr(self, token_spec["processor_method"])(match=match, line_number=line_number)
                    break
            else:
                if line.strip():
                    raise LexerException(f'Unable to parse "{line}" on line {line_number}')

    def _process_assignment(self, match: re.Match, line_number: int) -> None:
        """
        Process a variable assignment line

        :param match: Regex match of the assignment.
        """
        name: str = str(match["name"]).strip()
        equals = str(match["equals"]).strip() if match.groupdict().get("equals", None) else None
        assigned_stripped = str(match["value"]).strip() if match.groupdict().get("value", None) else None
        assigned = assigned_stripped or None
        self._parsed_data.append(
            (
                TokenName.ASSIGNMENT,
                Assignment(
                    name=name,
                    equals=equals,
                    assigned=assigned,
                    line_number=line_number,
                ),
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
                    content=str(match["comment"]).strip(),
                    line_number=line_number,
                ),
            )
        )

    def _process_cpm_parameter_validation(self, match: re.Match, line_number: int) -> None:
        """
        Process the provided parameter validation.

        :param match: Regex match of the parameter validation.
        """
        allow_characters: str | None = None
        if match["allowcharacters"]:
            allow_characters = str(match["allowcharacters"]).strip()

        self._parsed_data.append(
            (
                TokenName.CPM_PARAMETER_VALIDATION,
                CPMParameterValidation(
                    name=str(match["name"]),
                    source=str(match["source"]),
                    mandatory=str(match["mandatory"]),
                    allow_characters=allow_characters,
                    line_number=line_number,
                ),
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
                    name=str(match["name"]).strip(),
                    message=str(match["message"]).strip(),
                    code=int(match["code"]),
                    line_number=line_number,
                ),
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
                    name=str(match["name"].strip()),
                    line_number=line_number,
                ),
            )
        )

    def _process_transitions(self, match: re.Match, line_number: int) -> None:
        """
        Process the provided transitions.

        :param match: Regex match of the transitions.
        """
        self._parsed_data.append(
            (
                TokenName.TRANSITION,
                Transition(
                    current_state=str(match["current"]).strip(),
                    condition=str(match["condition"]).strip(),
                    next_state=str(match["next"]).strip(),
                    line_number=line_number,
                ),
            )
        )

    @property
    def tokens(
        self,
    ) -> list[
        tuple[
            TokenName,
            ALL_TOKEN_TYPES,
        ]
    ]:
        """A list of tokens found by the lexer."""
        if not self._parsed_data:
            self.process()
        return self._parsed_data
