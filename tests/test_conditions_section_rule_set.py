"""Tests for the conditions section rule set."""

import pytest

from tpc_plugin_parser.parser import Parser
from tpc_plugin_validator.rule_sets.conditions_section_rule_set import (
    ConditionsSectionRuleSet,
)
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestConditionsSectionRuleSet(object):
    """Tests for the debug information rule set."""

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
                        message='The token type "Transition" is not valid in this section, file: prompts.ini, section: conditions, line: 18.',
                    ),
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "failure" has been declared 2 times, file: prompts.ini, section: conditions.',
                    ),
                    ValidationResult(
                        rule="NameCaseMismatchViolation",
                        severity=Severity.WARNING,
                        message='The condition "Hello" is declared but is used as "hello", file: prompts.ini, section: conditions, line: 13.',
                    ),
                    ValidationResult(
                        rule="UnusedConditionViolation",
                        severity=Severity.WARNING,
                        message='The condition "Unused" is declared but is not used, file: prompts.ini, section: conditions, line: 19.',
                    ),
                    ValidationResult(
                        rule="InvalidWordViolation",
                        severity=Severity.CRITICAL,
                        message="The word 'CD' is reserved and cannot be used as a name in an assignment, file: prompts.ini, section: conditions, line: 22.",
                    ),
                    ValidationResult(
                        rule="UnusedConditionViolation",
                        severity=Severity.WARNING,
                        message='The condition "CD" is declared but is not used, file: prompts.ini, section: conditions, line: 22.',
                    ),
                    ValidationResult(
                        rule="InvalidWordViolation",
                        severity=Severity.CRITICAL,
                        message="The word 'sql' is reserved and cannot be used as a name in an assignment, file: prompts.ini, section: conditions, line: 23.",
                    ),
                    ValidationResult(
                        rule="UnusedConditionViolation",
                        severity=Severity.WARNING,
                        message='The condition "sql" is declared but is not used, file: prompts.ini, section: conditions, line: 23.',
                    ),
                ],
            ),
        ],
    )
    def test_conditions_section_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_results: list[ValidationResult],
    ) -> None:
        """
        Tests for the conditions section rule set.

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

        rule = ConditionsSectionRuleSet(prompts_file=parsed_prompts_file, process_file=parsed_process_file, config={})
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)

        for result in results:
            assert result in expected_results
