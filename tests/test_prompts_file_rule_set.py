"""Tests for the prompts file rule set."""

import pytest

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.prompts_file_rule_set import PromptsFileRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestPromptsFileRuleSets(object):
    """Tests for the prompts file rule set."""

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
                        message='The token type "Transition" is not valid in the "default" section, file: prompts.ini, line: 8.',
                    ),
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "conditions" has been declared as "Conditions", file: prompts.ini.',
                    ),
                ],
            ),
            (
                "tests/data/empty-process.ini",
                "tests/data/empty-prompts.ini",
                [
                    ValidationResult(
                        rule="MissingSectionViolation",
                        severity=Severity.CRITICAL,
                        message='"conditions" is a required section but this is missing, file: prompts.ini.',
                    ),
                ],
            ),
        ],
    )
    def test_prompts_file_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_results: list[ValidationResult],
    ) -> None:
        """
        Tests for the prompts file rule set.

        :param process_file: Path to the process file to use for the test case.
        :param prompts_file: Path to the prompts file to use for the test case.
        :param expected_results: List of expected ValidationResult
        """
        parser = Parser(process_file=process_file, prompts_file=prompts_file)
        process_file = parser.process_file
        prompts_file = parser.prompts_file

        rule = PromptsFileRuleSet(prompts_file=prompts_file, process_file=process_file, config={})
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)

        for result in results:
            assert result in expected_results
