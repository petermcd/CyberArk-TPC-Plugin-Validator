"""Tests for the parameters section rule set."""

import pytest

from tpc_plugin_parser.parser import Parser
from tpc_plugin_validator.rule_sets.parameters_section_rule_set import (
    ParametersSectionRuleSet,
)
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestParametersSectionRuleSet(object):
    """Tests for the parameters section rule set."""

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
                        message='The token type "Transition" is not valid in this section, file: process.ini, section: parameters, line: 63.',
                    ),
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='"SendHumanMin" is set to 1.0 and "SendHumanMax" is set to 0.0, "SendHumanMin" cannot be greater than "SendHumanMax", file: process.ini, section: parameters.',
                    ),
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "PromptTimeout" has been declared 2 times, file: process.ini, section: parameters.',
                    ),
                    ValidationResult(
                        rule="InvalidWordViolation",
                        severity=Severity.CRITICAL,
                        message="The word 'open' is reserved and cannot be used as a name in an assignment, file: process.ini, section: parameters, line: 68.",
                    ),
                ],
            ),
            (
                "tests/data/invalid-process-alt.ini",
                "tests/data/invalid-prompts.ini",
                [
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='"SendHumanMin" is set to -1.0 this cannot be less than 0, file: process.ini, section: parameters, line: 64.',
                    ),
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='"SendHumanMax" is set to -1.0 this cannot be less than 0, file: process.ini, section: parameters, line: 65.',
                    ),
                ],
            ),
            (
                "tests/data/invalid-process-alt2.ini",
                "tests/data/invalid-prompts.ini",
                [
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='"SendHumanMin" is set to "twenty-two", the value must be numerical, file: process.ini, section: parameters, line: 64.',
                    ),
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='"SendHumanMax" is set to "twenty-three", the value must be numerical, file: process.ini, section: parameters, line: 65.',
                    ),
                ],
            ),
        ],
    )
    def test_parameters_section_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_results: list[ValidationResult],
    ) -> None:
        """
        Tests for the parameters section rule set.

        :param process_file: Path to the process file to use for the test case.
        :param prompts_file: Path to the prompts file to use for the test case.
        :param expected_results: List of expected ValidationResult
        """
        with open(process_file, "r") as process_fh, open(prompts_file, "r") as prompts_fh:
            process_file_content = process_fh.read()
            prompts_file_content = prompts_fh.read()

        parser = Parser(process_file=process_file_content, prompts_file=prompts_file_content)
        parsed_process_file = parser.process_file
        parsed_prompts_file = parser.prompts_file

        rule = ParametersSectionRuleSet(prompts_file=parsed_prompts_file, process_file=parsed_process_file, config={})
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)

        for result in results:
            assert result in expected_results
