"""Tests for the process file rule set."""

import pytest

from tpc_plugin_parser.parser import Parser
from tpc_plugin_validator.rule_sets.process_file_rule_set import ProcessFileRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestProcessFileRuleSet(object):
    """Tests for the process rule set."""

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
                        message='The token type "Transition" is not valid in this section, file: process.ini, section: default, line: 8.',
                    ),
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "Debug Information" has been declared as "debug information", file: process.ini.',
                    ),
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "CPM Parameters Validation" has been declared as "cpm Parameters Validation", file: process.ini.',
                    ),
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "parameters" has been declared as "Parameters", file: process.ini.',
                    ),
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "transitions" has been declared as "Transitions", file: process.ini.',
                    ),
                    ValidationResult(
                        rule="InvalidSectionNameViolation",
                        severity=Severity.WARNING,
                        message='Invalid section "Dummy Section" identified, file: process.ini.',
                    ),
                ],
            ),
            (
                "tests/data/empty-process.ini",
                "tests/data/empty-prompts.ini",
                [
                    ValidationResult(
                        rule="MissingSectionViolation",
                        severity=Severity.WARNING,
                        message='"CPM Parameters Validation" is a required section but this is missing, file: process.ini.',
                    ),
                    ValidationResult(
                        rule="MissingSectionViolation",
                        severity=Severity.CRITICAL,
                        message='"states" is a required section but this is missing, file: process.ini.',
                    ),
                    ValidationResult(
                        rule="MissingSectionViolation",
                        severity=Severity.CRITICAL,
                        message='"transitions" is a required section but this is missing, file: process.ini.',
                    ),
                ],
            ),
        ],
    )
    def test_process_file_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_results: list[ValidationResult],
    ) -> None:
        """
        Tests for the process file rule set.

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

        rule = ProcessFileRuleSet(prompts_file=parsed_prompts_file, process_file=parsed_process_file, config={})
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)

        for result in results:
            assert result in expected_results
