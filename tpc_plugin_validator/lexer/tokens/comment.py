"""Class to hold the comment token."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Comment(object):
    """Dataclass to hold a comment."""
    line_number: int
    content: str
    token_name: str = 'Comment'
