"""Class to hold the fail state token."""
from dataclasses import dataclass


@dataclass(frozen=True)
class FailState(object):
    """Dataclass to hold a fail state."""
    line_number: int
    message: str
    code: int
