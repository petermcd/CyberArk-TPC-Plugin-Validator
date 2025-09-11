"""Enum to hold the allowed token names."""

from enum import Enum


class TokenName(Enum):
    """CLass to hold the token name."""
    ASSIGNMENT = 'ASSIGNMENT'
    COMMENT = 'COMMENT'
    EOF = 'EOF'
    FAIL_STATE = 'FAIL+STATE'
    SECTION_HEADER = 'SECTION_HEADER'
    STATE_TRANSITION = 'TRANSITION'
