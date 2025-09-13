"""Tests for the cpm parameter validations rule set."""

import pytest

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.cpm_parameter import CPMParameter
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestCPMParameterRuleSets(object):
    """Tests for the cpm parameter validations rule set."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_results",
        [
            (
                'tests/data/WARNING-CPMParameterNoSectionViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='CPMParameterNoSectionViolation',
                        severity=Severity.WARNING,
                        message='The process file does not contain a "CPM Parameters Validation" section.',
                    ),
                ],
            ),
            (
                'tests/data/WARNING-CPMParameterTokenViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='CPMParameterTokenViolation',
                        severity=Severity.WARNING,
                        message='The token type "State Transition" is not valid in the "CPM Parameters Validation" section, found on line 10.',
                    ),
                ],
            ),
            (
                'tests/data/OK-CPMParameter/process.ini',
                'tests/data/empty_prompts.ini',
                [],
            ),
        ],
    )
    def test_parameter_rules(self, process_file: str, prompts_file: str, expected_results: list[ValidationResult]) -> None:
        """
        Test parameter rule sets.

        :param process_file: The path to the process file.
        :param prompts_file: The path to the prompt file.
        :param expected_results: The expected validation results.
        """
        parser = Parser(process_file=process_file, prompts_file=prompts_file)
        process_content = parser.process_file
        prompts_content = parser.prompts_file

        rule = CPMParameter(prompts=prompts_content, process=process_content, config={})
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)
        for result, expected in zip(results, expected_results):
            assert result.rule == expected.rule
            assert result.severity == expected.severity
            assert result.message == expected.message

