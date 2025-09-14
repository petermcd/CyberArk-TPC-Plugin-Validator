"""Class to hold the state transition token."""
from dataclasses import dataclass

from tpc_plugin_validator.lexer.utilities.token_name import TokenName


@dataclass(frozen=True)
class StateTransition(object):
    """Dataclass to hold state transitions."""
    line_number: int
    from_state: str
    condition: str
    to_state: str
    token_name: str = TokenName.STATE_TRANSITION.value
