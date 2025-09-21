"""Tests for the debug information section rule set."""

import pytest

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.debug_information_section_rule_set import (
    DebugInformationSectionRuleSet,
)
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestDebugInformationSectionRuleSet(object):
    """Tests for the debug information section rule set."""

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
                        message='The token type "Transition" is not valid in the "Debug Information" section, file: process.ini, line: 73.',
                    ),
                    ValidationResult(
                        rule="ValueCaseViolation",
                        severity=Severity.WARNING,
                        message='The value for "DebugLogFullExecutionInfo" in the "Debug Information" section is set to "No" this should be in lower case, file: process.ini, line: 75.',
                    ),
                    ValidationResult(
                        rule="NameViolation",
                        severity=Severity.WARNING,
                        message='The setting "InvalidName" in the "Debug Information" section is not a valid "Debug Information" setting. Valid settings are: DebugLogFullParsingInfo, DebugLogFullExecutionInfo, DebugLogDetailBuiltInActions, ExpectLog, ConsoleOutput, file: process.ini, line: 79.',
                    ),
                    ValidationResult(
                        rule="NameCaseViolation",
                        severity=Severity.WARNING,
                        message='The setting "COnsoleOutput" in the "Debug Information" section should be set as "ConsoleOutput", file: process.ini, line: 78.',
                    ),
                    ValidationResult(
                        rule="NameCaseViolation",
                        severity=Severity.WARNING,
                        message='The setting "COnsoleOutput" in the "Debug Information" section should be set as "ConsoleOutput", file: process.ini, line: 80.',
                    ),
                    ValidationResult(
                        rule="ValueCaseViolation",
                        severity=Severity.WARNING,
                        message='The value for "COnsoleOutput" in the "Debug Information" section is set to "No" this should be in lower case, file: process.ini, line: 78.',
                    ),
                    ValidationResult(
                        rule="ValueCaseViolation",
                        severity=Severity.WARNING,
                        message='The value for "COnsoleOutput" in the "Debug Information" section is set to "No" this should be in lower case, file: process.ini, line: 80.',
                    ),
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='The value for "DebugLogDetailBuiltInActions" in the "Debug Information" section is set to "maybe" and is invalid. Valid values are "no" and "yes", file: process.ini, line: 76.',
                    ),
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.WARNING,
                        message='The value for "DebugLogFullParsingInfo" in the "Debug Information" section is blank. Setting should be explicitly set to "no", file: process.ini, line: 74.',
                    ),
                    ValidationResult(
                        rule="LoggingEnabledViolation",
                        severity=Severity.CRITICAL,
                        message='The value for "ExpectLog" in the "Debug Information" section is set to "yes". It is recommended to set all "Debug Information" settings to "no" for production environments, file: process.ini, line: 77.',
                    ),
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "COnsoleOutput" has been declared 2 times, file: process.ini.',
                    ),
                ],
            ),
        ],
    )
    def test_debug_information_logging_section_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_results: list[ValidationResult],
    ) -> None:
        """
        Tests for the debug information section rule set.

        :param process_file: Path to the process file to use for the test case.
        :param prompts_file: Path to the prompts file to use for the test case.
        :param expected_results: List of expected ValidationResult
        """
        parser = Parser(process_file=process_file, prompts_file=prompts_file)
        process_file = parser.process_file
        prompts_file = parser.prompts_file

        rule = DebugInformationSectionRuleSet(prompts_file=prompts_file, process_file=process_file, config={})
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)

        for result in results:
            assert result in expected_results
