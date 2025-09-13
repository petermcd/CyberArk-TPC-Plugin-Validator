"""Enum to hold the allowed token names."""

from enum import Enum


class TokenName(Enum):
    """CLass to hold the token name."""
    ASSIGNMENT = 'ASSIGNMENT'
    COMMENT = 'COMMENT'
    FAIL_STATE = 'FAIL_STATE'
    CPM_PARAMETER_VALIDATION = 'CPM_PARAMETER_VALIDATION',
    SECTION_HEADER = 'SECTION_HEADER'
    STATE_TRANSITION = 'STATE_TRANSITION'
