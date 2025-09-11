"""Module to hold the Prompts dataclass."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Process(object):
    """Class to hold the parsed process file."""

    sections: list[str]

    state_keys = list[str]
    states: dict[str, str]

    transitions: list[tuple[str, str, str]]

    parameter_validation_keys: list[str]
    parameter_validations: dict[str, str]

    parameter_keys: list[str]
    parameters: dict[str, str]

    debug_keys: list[str]
    debug: dict[str, str]
