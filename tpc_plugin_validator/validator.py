"""Class to manage validations."""

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.logging import Logging
from tpc_plugin_validator.rule_sets.prompts import Prompts
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class Validator(object):
    """Class to manage validations."""

    __slots__ = (
        '_config',
        '_parser',
        '_rule_sets',
        '_validations',
    )

    def __init__(self, parser: Parser, config: dict[str, dict[str, str]]) -> None:
        """
        Standard init for the Validator class.

        :param parser: Parser object
        """
        self._config: dict[str, dict[str, str]] = config
        self._parser: Parser = parser
        self._validations: list[ValidationResult] = []
        self._rule_sets = (
            Prompts,
            Logging,
        )

    def validate(self) -> None:
        """Execute validations."""
        for rule_set in self._rule_sets:
            config = self._config.get('logging', {})
            validator = rule_set(process=self._parser.process_file, prompts=self._parser.prompts_file, config=config)
            self._validations = self._validations + validator.validate()
