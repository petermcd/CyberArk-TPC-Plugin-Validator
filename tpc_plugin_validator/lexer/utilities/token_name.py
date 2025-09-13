"""Enum to hold the allowed token names."""

from enum import Enum


class TokenName(Enum):
    """CLass to hold the token name."""
    ASSIGNMENT = 'Assignment'
    COMMENT = 'Comment'
    FAIL_STATE = 'FAIL STATE'
    CPM_PARAMETER_VALIDATION = 'CPM Parameter Validation'
    SECTION_HEADER = 'Section Header'
    STATE_TRANSITION = 'State Transition'
