"""Class to manage validations."""

from typing import Callable

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.conditions_section_rule_set import (
    ConditionsSectionRuleSet,
)
from tpc_plugin_validator.rule_sets.cpm_parameters_validation_section_rule_set import (
    CPMParametersValidationSectionRuleSet,
)
from tpc_plugin_validator.rule_sets.debug_information_section_rule_set import (
    DebugInformationSectionRuleSet,
)
from tpc_plugin_validator.rule_sets.parameters_section_rule_set import (
    ParametersSectionRuleSet,
)
from tpc_plugin_validator.rule_sets.process_file_rule_set import ProcessFileRuleSet
from tpc_plugin_validator.rule_sets.prompts_file_rule_set import PromptsFileRuleSet
from tpc_plugin_validator.rule_sets.states_section_rule_set import StatesSectionRuleSet
from tpc_plugin_validator.rule_sets.transitions_section_rule_set import (
    TransitionsSectionRuleSet,
)
from tpc_plugin_validator.utilities.types import CONFIG_TYPE
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class Validator(object):
    """Class to manage validations."""

    __slots__ = (
        "_config",
        "_parser",
        "_rule_sets",
        "_validations",
    )

    def __init__(self, parser: Parser, config: CONFIG_TYPE) -> None:
        """
        Standard init for the Validator class.

        :param parser: Parser object
        """
        self._config: CONFIG_TYPE = config
        self._parser: Parser = parser
        self._validations: list[ValidationResult] = []
        self._rule_sets: set[Callable] = {
            ConditionsSectionRuleSet,
            CPMParametersValidationSectionRuleSet,
            DebugInformationSectionRuleSet,
            ParametersSectionRuleSet,
            ProcessFileRuleSet,
            PromptsFileRuleSet,
            StatesSectionRuleSet,
            TransitionsSectionRuleSet,
        }

    def get_violations(self) -> list[ValidationResult]:
        """
        Fetch a list of violations.

        :return: List of ValidationResult
        """
        return self._validations

    def validate(self) -> None:
        """Execute validations."""
        for rule_set in self._rule_sets:
            validator = rule_set(
                process_file=self._parser.process_file,
                prompts_file=self._parser.prompts_file,
                config=self._config,
            )
            validator.validate()
            self._validations = self._validations + validator.get_violations()
