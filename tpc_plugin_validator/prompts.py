"""Module to hold the Process dataclass."""
from dataclasses import dataclass


@dataclass
class Prompts(object):
    """Class to hold the parsed prompts file."""
    sections: list[str]
    conditions: dict[str, list[str]]
