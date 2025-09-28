"""Tests for the debug information section rule set."""

import pytest

from tpc_plugin_parser.parser import Parser
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
                        message='The token type "Transition" is not valid in this section, file: process.ini, section: Debug Information, line: 73.',
                    ),
                    ValidationResult(
                        rule="ValueCaseViolation",
                        severity=Severity.WARNING,
                        message='The value for "DebugLogFullExecutionInfo" is set to "No" this should be in lower case, file: process.ini, section: Debug Information, line: 75.',
                    ),
                    ValidationResult(
                        rule="NameViolation",
                        severity=Severity.WARNING,
                        message='The setting "InvalidName" is not a valid setting. Valid settings are: DebugLogFullParsingInfo, DebugLogFullExecutionInfo, DebugLogDetailBuiltInActions, ExpectLog, ConsoleOutput, file: process.ini, section: Debug Information, line: 79.',
                    ),
                    ValidationResult(
                        rule="NameCaseViolation",
                        severity=Severity.WARNING,
                        message='The setting "COnsoleOutput" should be set as "ConsoleOutput", file: process.ini, section: Debug Information, line: 78.',
                    ),
                    ValidationResult(
                        rule="NameCaseViolation",
                        severity=Severity.WARNING,
                        message='The setting "COnsoleOutput" should be set as "ConsoleOutput", file: process.ini, section: Debug Information, line: 80.',
                    ),
                    ValidationResult(
                        rule="ValueCaseViolation",
                        severity=Severity.WARNING,
                        message='The value for "COnsoleOutput" is set to "No" this should be in lower case, file: process.ini, section: Debug Information, line: 78.',
                    ),
                    ValidationResult(
                        rule="ValueCaseViolation",
                        severity=Severity.WARNING,
                        message='The value for "COnsoleOutput" is set to "No" this should be in lower case, file: process.ini, section: Debug Information, line: 80.',
                    ),
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='The value for "DebugLogDetailBuiltInActions" is set to "maybe" and is invalid. Valid values are "no" and "yes", file: process.ini, section: Debug Information, line: 76.',
                    ),
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.WARNING,
                        message='The value for "DebugLogFullParsingInfo" is blank. Setting should be explicitly set to "no", file: process.ini, section: Debug Information, line: 74.',
                    ),
                    ValidationResult(
                        rule="LoggingEnabledViolation",
                        severity=Severity.CRITICAL,
                        message='The value for "ExpectLog" is set to "yes". It is recommended to set all settings in this section to "no" for production environments, file: process.ini, section: Debug Information, line: 77.',
                    ),
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "COnsoleOutput" has been declared 2 times, file: process.ini, section: Debug Information.',
                    ),
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed, file: process.ini, section: Debug Information, line: 81.",
                    ),
                    ValidationResult(
                        rule="InvalidWordViolation",
                        severity=Severity.CRITICAL,
                        message="The word 'debug' is reserved and cannot be used as a name in an assignment, file: process.ini, section: Debug Information, line: 82.",
                    ),
                    ValidationResult(
                        rule="NameViolation",
                        severity=Severity.WARNING,
                        message='The setting "debug" is not a valid setting. Valid settings are: DebugLogFullParsingInfo, DebugLogFullExecutionInfo, DebugLogDetailBuiltInActions, ExpectLog, ConsoleOutput, file: process.ini, section: Debug Information, line: 82.',
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
        with open(process_file, "r") as process_fh, open(prompts_file, "r") as prompts_fh:
            process_file_content = process_fh.read()
            prompts_file_content = prompts_fh.read()

        parser = Parser(process_file=process_file_content, prompts_file=prompts_file_content)
        parsed_process_file = parser.process_file
        parsed_prompts_file = parser.prompts_file

        rule = DebugInformationSectionRuleSet(
            prompts_file=parsed_prompts_file, process_file=parsed_process_file, config={}
        )
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)

        for result in results:
            assert result in expected_results
