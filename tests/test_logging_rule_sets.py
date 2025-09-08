"""Test logging rule sets."""
import pytest

from tpc_plugin_validator.parser import Parser
from tpc_plugin_validator.severity import Severity
from tpc_plugin_validator.validation_result import ValidationResult


class TestLoggingRuleSets():
    @pytest.mark.parametrize(
        "process_file, prompts_file, enabled, expected_results",
        [
            (
                "tests/data/WARNING-LoggingValueCaseViolation/process.ini",
                "tests/data/WARNING-LoggingValueCaseViolation/prompts.ini",
                True,
                [
                    ValidationResult(
                        rule='LoggingValueCaseViolation',
                        severity=Severity.WARNING,
                        message='The logging value for "DebugLogFullExecutionInfo" is set to "No" and is not in lower case. Ensure all logging settings are in lower case.'
                    ),
                ],
            ),
            (
                "tests/data/OK-LoggingNoSection/process.ini",
                "tests/data/OK-LoggingNoSection/prompts.ini",
                True,
                [
                    ValidationResult(
                        rule='LoggingNoSection',
                        severity=Severity.INFO,
                        message='The process file does not contain a "Debug Information" section, therefore, logging is disabled.',
                    ),
                ],
            ),
            (
                "tests/data/WARNING-LoggingSettingNameViolation/process.ini",
                "tests/data/WARNING-LoggingSettingNameViolation/prompts.ini",
                True,
                [
                    ValidationResult(
                        rule='LoggingSettingNameViolation',
                        severity=Severity.WARNING,
                        message='The logging setting "InvalidName" is not a valid logging setting. Valid settings are: DebugLogFullParsingInfo, DebugLogFullExecutionInfo, DebugLogDetailBuiltInActions, ExpectLog, ConsoleOutput.',
                    ),
                ],
            ),
            (
                "tests/data/OK-logging/process.ini",
                "tests/data/OK-logging/prompts.ini",
                True,
                [],
            ),
            (
                "tests/data/WARNING-LoggingValueViolation/process.ini",
                "tests/data/WARNING-LoggingValueViolation/prompts.ini",
                True,
                [
                    ValidationResult(
                        rule='LoggingValueViolation',
                        severity=Severity.CRITICAL,
                        message='The logging value for "DebugLogDetailBuiltInActions" is set to "maybe" and is invalid. Valid values are "no" and "yes".',
                    ),
                ],
            ),
            (
                "tests/data/CRITICAL-LoggingEnabledViolation/process.ini",
                "tests/data/CRITICAL-LoggingEnabledViolation/prompts.ini",
                True,
                [
                    ValidationResult(
                        rule='LoggingEnabledViolation',
                        severity=Severity.CRITICAL,
                        message='The logging value for "ExpectLog" is set to "yes". It is recommended to set all logging settings to "no" for production environments.',
                    ),
                ],
            ),
            (
                "tests/data/CRITICAL-LoggingEnabledViolation/process.ini",
                "tests/data/CRITICAL-LoggingEnabledViolation/prompts.ini",
                False,
                [
                    ValidationResult(
                        rule='LoggingEnabledViolation',
                        severity=Severity.INFO,
                        message='The logging value for "ExpectLog" is set to "yes". It is recommended to set all logging settings to "no" for production environments.',
                    ),
                ],
            ),
        ],
    )
    def test_logging_rules(self, process_file: str, prompts_file: str, enabled: bool, expected_results: list[ValidationResult]) -> None:
        """
        Test logging rule sets.

        :param process_file: The path to the process file.
        :param prompts_file: The path to the prompt file.
        :param expected_results: The expected validation results.
        """
        from tpc_plugin_validator.rules.logging_validation import LoggingValidation

        parser = Parser(process_file=process_file, prompts_file=prompts_file)
        process_content = parser.process_file
        prompts_content = parser.prompts_file

        rule = LoggingValidation(prompts=prompts_content, process=process_content, enabled=enabled)
        results = rule.validate()

        assert len(results) == len(expected_results)
        for result, expected in zip(results, expected_results):
            assert result.rule == expected.rule
            assert result.severity == expected.severity
            assert result.message == expected.message