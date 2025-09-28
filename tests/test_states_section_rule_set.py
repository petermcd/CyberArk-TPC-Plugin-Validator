"""Tests for the states section rule set."""

import pytest

from tpc_plugin_parser.parser import Parser
from tpc_plugin_validator.rule_sets.states_section_rule_set import StatesSectionRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestStatesSectionRuleSet(object):
    """Tests for the states rule set."""

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
                "tests/data/valid-prompts.ini",
                [
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.WARNING,
                        message='The token type "Transition" is not valid in this section, file: process.ini, section: states, line: 13.',
                    ),
                    ValidationResult(
                        rule="NameCaseViolation",
                        severity=Severity.CRITICAL,
                        message='The END state has been declared as "end", the END state should be in upper case, file: process.ini, section: states, line: 19.',
                    ),
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='The END state has been assigned the value "123", the END state should not have a value, file: process.ini, section: states, line: 19.',
                    ),
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='The fail state "SomeFailure" has an invalid failure code of "123", the failure code should be between 1000 and 9999, file: process.ini, section: states, line: 17.',
                    ),
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='The fail state "AnotherFailure" has an invalid failure code of "123", the failure code should be between 1000 and 9999, file: process.ini, section: states, line: 18.',
                    ),
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.WARNING,
                        message='The code "123" has been assigned 2 times to failure states, file: process.ini, section: states.',
                    ),
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "Wait" has been declared 2 times, file: process.ini, section: states.',
                    ),
                    ValidationResult(
                        rule="InvalidWordViolation",
                        severity=Severity.CRITICAL,
                        message="The word 'source' is reserved and cannot be used as a name in an assignment, file: process.ini, section: states, line: 22.",
                    ),
                ],
            ),
        ],
    )
    def test_states_section_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_results: list[ValidationResult],
    ) -> None:
        """
        Tests for the states section rule set.

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

        rule = StatesSectionRuleSet(prompts_file=parsed_prompts_file, process_file=parsed_process_file, config={})

        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)

        for result in results:
            assert result in expected_results
