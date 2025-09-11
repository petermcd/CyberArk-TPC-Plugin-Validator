"""Class to hold the fail state token."""
from dataclasses import dataclass


@dataclass(frozen=True)
class FailState(object):
    """Dataclass to hold a fail state."""
    message: str
    code: int
