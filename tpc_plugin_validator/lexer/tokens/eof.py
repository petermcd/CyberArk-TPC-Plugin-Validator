"""Class to hold the end of file token."""
from dataclasses import dataclass


@dataclass(frozen=True)
class EOF(object):
    """Dataclass to hold end of file."""
    pass
