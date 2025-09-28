"""Tests for the transitions section rule set."""

import pytest

from tpc_plugin_parser.parser import Parser
from tpc_plugin_validator.rule_sets.transitions_section_rule_set import (
    TransitionsSectionRuleSet,
)
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestTransitionsSectionRuleSet(object):
    """Tests for the transitions section rule set."""

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
                        message='The token type "Assignment" is not valid in this section, file: process.ini, section: transitions, line: 40.',
                    ),
                    ValidationResult(
                        rule="DuplicateTransitionViolation",
                        severity=Severity.WARNING,
                        message='The transition "Init,hello,wait" has been declared 2 times, a transition tuple must be unique, file: process.ini, section: transitions.',
                    ),
                    ValidationResult(
                        rule="InvalidTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The state "wait" attempts to transition to "NoNext" which does not exist, file: process.ini, section: transitions, line: 36.',
                    ),
                    ValidationResult(
                        rule="InvalidTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The state "NoPrevious" does not have a valid path leading to it, file: process.ini, section: transitions, line: 37.',
                    ),
                ],
            ),
        ],
    )
    def test_transitions_section_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_results: list[ValidationResult],
    ) -> None:
        """
        Tests for the transitions section rule set.

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

        rule = TransitionsSectionRuleSet(prompts_file=parsed_prompts_file, process_file=parsed_process_file, config={})
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)

        for result in results:
            assert result in expected_results
