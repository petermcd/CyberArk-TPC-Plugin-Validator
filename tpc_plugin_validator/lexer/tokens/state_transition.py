"""Class to hold the state transition token."""
from dataclasses import dataclass


@dataclass(frozen=True)
class StateTransition(object):
    """Dataclass to hold state transitions."""
    line_number: int
    from_state: str
    condition: str
    to_state: str
