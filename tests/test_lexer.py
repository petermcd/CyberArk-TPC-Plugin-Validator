"""Test the lexer."""
import pytest

from tpc_plugin_validator.lexer.lexer import Lexer
from tpc_plugin_validator.lexer.tokens.assignment import Assignment
from tpc_plugin_validator.lexer.tokens.comment import Comment
from tpc_plugin_validator.lexer.tokens.fail_state import FailState
from tpc_plugin_validator.lexer.tokens.section_header import SectionHeader
from tpc_plugin_validator.lexer.tokens.state_transition import StateTransition
from tpc_plugin_validator.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.utilities.exceptions import LexerException


class TestLexer(object):
    """Test the lexer."""

    @pytest.mark.parametrize(
        'line,expected_token_list',
        [
            (
                'TestVar',
                [
                    (
                        TokenName.ASSIGNMENT,
                        Assignment(
                            line_number=1,
                            name='TestVar',
                            equals=None,
                            assigned=None,
                        ),
                    ),
                ],
            ),
            (
                'testvar    =   ',
                [
                    (
                        TokenName.ASSIGNMENT,
                        Assignment(
                            line_number=1,
                            name='testvar',
                            equals='=',
                            assigned=None,
                        ),
                    ),
                ],
            ),
            (
                'test_var = 123',
                [
                    (
                        TokenName.ASSIGNMENT,
                        Assignment(
                            line_number=1,
                            name='test_var',
                            equals='=',
                            assigned='123',
                        ),
                    ),
                ],
            ),
            (
                '# this is a standard comment     ',
                [
                    (
                        TokenName.COMMENT,
                        Comment(
                            line_number=1,
                            content='# this is a standard comment',
                        ),
                    ),
                ],
            ),
            (
                ';this is a standard comment',
                [
                    (
                        TokenName.COMMENT,
                        Comment(
                            line_number=1,
                            content=';this is a standard comment',
                        ),
                    ),
                ],
            ),
            (
                "FAIL('This is a standard fail state', 1234)",
                [
                    (
                        TokenName.FAIL_STATE,
                        FailState(
                            line_number=1,
                            message='This is a standard fail state',
                            code=1234,
                        ),
                    ),
                ],
            ),
            (
                "FAIL  ('This is a standard fail state, isn\'t it?',     2468)",
                [
                    (
                        TokenName.FAIL_STATE,
                        FailState(
                            line_number=1,
                            message='This is a standard fail state, isn\'t it?',
                            code=2468,
                        ),
                    ),
                ],
            ),
            (
                '[Some Section Header]',
                [
                    (
                        TokenName.SECTION_HEADER,
                        SectionHeader(
                            line_number=1,
                            name='Some Section Header',
                        ),
                    ),
                ],
            ),
            (
                '   [Some Section Header]    ',
                [
                    (
                        TokenName.SECTION_HEADER,
                        SectionHeader(
                            line_number=1,
                            name='Some Section Header',
                        ),
                    ),
                ],
            ),
            (
                'state1,condition,state2',
                [
                    (
                        TokenName.STATE_TRANSITION,
                        StateTransition(
                            line_number=1,
                            from_state='state1',
                            condition='condition',
                            to_state='state2',
                        ),
                    ),
                ],
            ),
            (
                ' state_1    ,   condition2    , STATE2   ',
                [
                    (
                        TokenName.STATE_TRANSITION,
                        StateTransition(
                            line_number=1,
                            from_state='state_1',
                            condition='condition2',
                            to_state='STATE2',
                        ),
                    ),
                ],
            ),
            (
                '[Some Section Header]\r\rTestVar\r',
                [
                    (
                        TokenName.SECTION_HEADER,
                        SectionHeader(
                            line_number=1,
                            name='Some Section Header',
                        ),
                    ),
                    (
                        TokenName.ASSIGNMENT,
                        Assignment(
                            line_number=3,
                            name='TestVar',
                            equals=None,
                            assigned=None,
                        ),
                    ),
                ],
            ),
        ],
    )
    def test_token(self, line: str, expected_token_list):
        """
        Test to ensure that a token parses ok.

        :param line: The line to be parsed.
        :param expected_token: A copy of the object we expect to receive back.
        """
        lexer = Lexer(source=line)
        lexer.process()
        tokens = lexer.tokens
        assert tokens == expected_token_list

    @pytest.mark.parametrize(
        'line, expected_exception, expected_error',
        [
            (
                'This line will not match',
                LexerException,
                'Unable to parse "This line will not match" on line 1',
            ),
        ],
    )
    def test_unmatched_lines(self, line: str, expected_exception: Exception, expected_error: str):
        """
        Test to ensure that the lexer fails in an expected way when it identifies a line it cannot deal with.

        :param line: The line to be parsed.
        :param expected_exception: The exception that should be thrown.
        :param expected_error: The message the exception should provide.
        """
        lex = Lexer(source=line)
        with pytest.raises(expected_exception) as excinfo:
            lex.process()
        assert str(excinfo.value) == expected_error
