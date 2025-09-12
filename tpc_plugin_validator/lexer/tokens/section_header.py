"""Class to hold the section header token."""
from dataclasses import dataclass


@dataclass(frozen=True)
class SectionHeader(object):
    """Dataclass to hold a section header name."""
    line_number: int
    name: str
    token_name: str = 'Section Header'
