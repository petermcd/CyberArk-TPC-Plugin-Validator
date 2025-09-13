"""Class to hold the parameter validation token."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ParameterValidation(object):
    """Dataclass to hold variable parameter validation details."""
    line_number: int
    name: str
    source: str
    mandatory: str
    allow_characters: str | None = None
    token_name: str = 'Parameter Validation'
