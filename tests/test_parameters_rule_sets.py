"""Tests for the parameters rule set."""

import pytest

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.parameters import Parameters
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestParameterRuleSets(object):
    """Tests for the parameters rule set."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_results",
        [
            (
                'tests/data/OK-Parameters/process.ini',
                'tests/data/empty_prompts.ini',
                [],
            ),
            (
                'tests/data/CRITICAL-ParametersNoParametersSectionViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='ParametersNoParametersSectionViolation',
                        severity=Severity.CRITICAL,
                        message='The process file does not contain a "parameters" section.',
                    )
                ],
            ),
            (
                'tests/data/WARNING-ParametersDuplicateParametersViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='ParametersDuplicateParametersViolation',
                        severity=Severity.WARNING,
                        message='The assignment "PromptTimeout" has been declared 2 times in the process file.',
                    )
                ],
            ),
            (
                'tests/data/CRITICAL-ParameterMinGreaterThanMaxViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='ParameterMinGreaterThanMaxViolation',
                        severity=Severity.CRITICAL,
                        message='SendHumanMin is set to 1.0 and SendHumanMax is set to 0.0, SendHumanMin cannot be greater than SendHumanMax.',
                    )
                ],
            ),
            (
                'tests/data/CRITICAL-ParameterMinLessThanZeroViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='ParameterMinLessThanZeroViolation',
                        severity=Severity.CRITICAL,
                        message='SendHumanMin is set to -1.0 this cannot be less than 0.',
                    )
                ],
            ),
            (
                'tests/data/CRITICAL-ParameterMaxLessThanZeroViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='ParameterMaxLessThanZeroViolation',
                        severity=Severity.CRITICAL,
                        message='SendHumanMax is set to -1.0 this cannot be less than 0.',
                    )
                ],
            ),
        ],
    )
    def test_parameters_rules(self, process_file: str, prompts_file: str, expected_results: list[ValidationResult]) -> None:
        """
        Test parameters rule sets.

        :param process_file: The path to the process file.
        :param prompts_file: The path to the prompt file.
        :param expected_results: The expected validation results.
        """
        parser = Parser(process_file=process_file, prompts_file=prompts_file)
        process_content = parser.process_file
        prompts_content = parser.prompts_file

        rule = Parameters(prompts=prompts_content, process=process_content, config={})
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)
        for result, expected in zip(results, expected_results):
            assert result.rule == expected.rule
            assert result.severity == expected.severity
            assert result.message == expected.message

