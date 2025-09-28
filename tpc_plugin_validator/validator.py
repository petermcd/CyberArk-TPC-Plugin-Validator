"""Class to manage validations."""

import os
from typing import Callable

from tpc_plugin_parser.parser import Parser
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

    def __init__(self, process_file_content: str, prompts_file_content: str, config: CONFIG_TYPE) -> None:
        """
        Standard init for the Validator class.

        :param process_file_content: Content for the process file.
        :param prompts_file_content: Content for the prompts file.
        :param config: Configuration
        """
        self._config: CONFIG_TYPE = config
        self._parser: Parser = Parser(
            process_file=process_file_content,
            prompts_file=prompts_file_content,
        )
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

    @classmethod
    def with_file(cls, process_file_path: str, prompts_file_path: str, config: CONFIG_TYPE) -> "Validator":
        """
        Set the file to be validated.

        :param process_file_path: Path to the process file.
        :param prompts_file_path: Path to the prompts file.
        :param config: Configuration

        :return: Self
        """
        if not os.path.isfile(process_file_path):
            raise FileNotFoundError(f"Process file not found: {process_file_path}")

        if not os.path.isfile(prompts_file_path):
            raise FileNotFoundError(f"Process file not found: {prompts_file_path}")

        with open(process_file_path, "r", encoding="utf-8") as process_file:
            process_file_content: str = process_file.read()

        with open(prompts_file_path, "r", encoding="utf-8") as prompts_file:
            prompts_file_content: str = prompts_file.read()

        return Validator(
            process_file_content=process_file_content, prompts_file_content=prompts_file_content, config=config
        )
