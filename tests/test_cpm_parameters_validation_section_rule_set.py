"""Tests for the CPM Parameters Validation section rule set."""

import pytest

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.cpm_parameters_validation_section_rule_set import (
    CPMParametersValidationSectionRuleSet,
)
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestCPMParametersValidationSectionRuleSet(object):
    """Tests for the CPM Parameters Validation section rule set."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_results",
        [
            (
                "tests/data/valid-process.ini",
                "tests/data/valid-prompts.ini",
                [],
            ),
            (
                "tests/data/invalid-process.ini",
                "tests/data/invalid-prompts.ini",
                [
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.WARNING,
                        message='The token type "Transition" is not valid in this section, file: process.ini, section: CPM Parameters Validation, line: 53.',
                    ),
                    ValidationResult(
                        rule="UnusedParameterViolation",
                        severity=Severity.WARNING,
                        message='The parameter "extrapass2\\Username" has been validated but is not used, file: process.ini, section: CPM Parameters Validation, line: 54.',
                    ),
                    ValidationResult(
                        rule="UnusedParameterViolation",
                        severity=Severity.WARNING,
                        message='The parameter "extrapass2\\Username" has been validated but is not used, file: process.ini, section: CPM Parameters Validation, line: 56.',
                    ),
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "extrapass2\\Username" has been declared 2 times, file: process.ini, section: CPM Parameters Validation.',
                    ),
                ],
            ),
        ],
    )
    def test_cpm_parameters_validation_section_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_results: list[ValidationResult],
    ) -> None:
        """
        Tests for the CPM Parameters Validation section rule set.

        :param process_file: Path to the process file to use for the test case.
        :param prompts_file: Path to the prompts file to use for the test case.
        :param expected_results: List of expected ValidationResult
        """
        parser = Parser(process_file=process_file, prompts_file=prompts_file)
        process_file = parser.process_file
        prompts_file = parser.prompts_file

        rule = CPMParametersValidationSectionRuleSet(prompts_file=prompts_file, process_file=process_file, config={})
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)

        for result in results:
            assert result in expected_results
