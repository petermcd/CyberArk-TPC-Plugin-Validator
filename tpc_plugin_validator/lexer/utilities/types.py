"""Module for aggregating all token types used in the lexer."""

from typing import TypedDict
import re

from tpc_plugin_validator.lexer.tokens.assignment import Assignment
from tpc_plugin_validator.lexer.tokens.comment import Comment
from tpc_plugin_validator.lexer.tokens.cpm_parameter_validation import (
    CPMParameterValidation,
)
from tpc_plugin_validator.lexer.tokens.fail_state import FailState
from tpc_plugin_validator.lexer.tokens.section_header import SectionHeader
from tpc_plugin_validator.lexer.tokens.transition import Transition
from tpc_plugin_validator.lexer.utilities.token_name import TokenName

ALL_TOKEN_TYPES = Assignment | Comment | FailState | CPMParameterValidation | SectionHeader | Transition


class TokenSpecs(TypedDict):
    pattern: re.Pattern
    token_name: TokenName
    processor_method: str
