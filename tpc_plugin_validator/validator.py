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
from tpc_plugin_validator.utilities.exceptions import ProgrammingError
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class Validator(object):
    """Class to manage validations."""

    __slots__ = (
        "_config",
        "_process",
        "_prompts",
        "_rule_sets",
        "_violations",
    )

    def __init__(self, process_file_content: str | None = None, prompts_file_content: str | None = None) -> None:
        """
        Standard init for the Validator class.

        :param process_file_content: Content for the process file.
        :param prompts_file_content: Content for the prompts file.
        """
        if not any([process_file_content, prompts_file_content]):
            raise ProgrammingError('At least one of process file and prompts file required.')

        if process_file_content is not None:
            self._process: Parser = Parser(
                file_contents=process_file_content,
            ).parsed_file

        if prompts_file_content is not None:
            self._prompts: Parser = Parser(
                file_contents=prompts_file_content,
            ).parsed_file

        self._violations: list[ValidationResult] = []
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
        return self._violations

    def validate(self) -> None:
        """Execute validations."""
        for rule_set in self._rule_sets:
            validator = rule_set(
                process_file=self._process,
                prompts_file=self._prompts,
            )
            validator.validate()
            self._violations = self.sort_violations(self._violations + validator.get_violations())

    @classmethod
    def sort_violations(cls, violations: list[ValidationResult]) -> list[ValidationResult]:
        """
        Sort violations by file, section, and line.

        :param violations: List of ValidationResult

        :return: Sorted list of ValidationResult
        """
        return sorted(
            violations,
            key=lambda violation: (
                str(violation.file) if violation.file is not None else "",
                str(violation.section) if violation.section is not None else "",
                violation.line if violation.line is not None else -1,
            ),
        )

    @classmethod
    def with_file(cls, process_file_path: str | None, prompts_file_path: str | None) -> "Validator":
        """
        Set the file to be validated.

        :param process_file_path: Path to the process file.
        :param prompts_file_path: Path to the prompts file.

        :return: Self
        """
        if process_file_path and not os.path.isfile(process_file_path):
            raise FileNotFoundError(f"The process file was not found: {process_file_path}")

        if prompts_file_path and not os.path.isfile(prompts_file_path):
            raise FileNotFoundError(f"The prompts file was not found: {prompts_file_path}")

        process_file_content: str | None = None
        prompts_file_content: str | None = None

        if process_file_path:
            with open(process_file_path, "r", encoding="utf-8") as process_file:
                process_file_content: str = process_file.read()

        if process_file_path:
            with open(prompts_file_path, "r", encoding="utf-8") as prompts_file:
                prompts_file_content: str = prompts_file.read()

        return Validator(
            process_file_content=process_file_content, prompts_file_content=prompts_file_content
        )
