"""Class to hold the assignment token."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Assignment(object):
    """Dataclass to hold variable assignment details."""
    line_number: int
    name: str
    equals: str | None = None
    assigned: str | None = None
