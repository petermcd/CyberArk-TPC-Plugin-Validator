"""Tests for the debug information section rule set."""

import pytest

from tpc_plugin_validator.validator import Validator
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestDebugInformationSectionRuleSet(object):
    """Tests for the debug information rule set."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_violations",
        [
            (
                "tests/data/debug-information-invalid-process.ini",
                "tests/data/debug-information-invalid-prompts.ini",
                [
                    # Test for ensuring duplicate assignments are caught.
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "ExpectLog" has been declared 2 times.',
                        file="process.ini",
                        section="Debug Information",
                    ),
                    # Test for ensuring blank values are caught when no = present
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.WARNING,
                        message='The value for "DebugLogFullParsingInfo" is blank. Setting should be explicitly set to "no".',
                        file="process.ini",
                        section="Debug Information",
                        line=44,
                    ),
                    # Test for ensuring blank values are caught when no = present
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.WARNING,
                        message='The value for "DebugLogFullExecutionInfo" is blank. Setting should be explicitly set to "no".',
                        file="process.ini",
                        section="Debug Information",
                        line=45,
                    ),
                    # Test for ensuring setting name case violation is caught.
                    ValidationResult(
                        rule="NameCaseViolation",
                        severity=Severity.WARNING,
                        message='The setting "expectlog" should be set as "ExpectLog".',
                        file="process.ini",
                        section="Debug Information",
                        line=48,
                    ),
                    # Test for ensuring setting value case violation is caught.
                    ValidationResult(
                        rule="ValueCaseViolation",
                        severity=Severity.WARNING,
                        message='The value for "expectlog" is set to "Yes" this should be in lower case.',
                        file="process.ini",
                        section="Debug Information",
                        line=48,
                    ),
                    # Test for ensuring logging is disabled.
                    ValidationResult(
                        rule="LoggingEnabledViolation",
                        severity=Severity.CRITICAL,
                        message='The value for "expectlog" is set to "Yes". It is recommended to set all settings in this section to "no" for production environments.',
                        file="process.ini",
                        section="Debug Information",
                        line=48,
                    ),
                    # Test for ensuring invalid setting values are caught.
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='The value for "ConsoleOutput" is set to "Maybe" and is invalid. Valid values are "no" and "yes".',
                        file="process.ini",
                        section="Debug Information",
                        line=49,
                    ),
                    # Test invalid token type in debug information section are caught.
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.CRITICAL,
                        message='The token type "Transition" is not valid in the "Debug Information" section.',
                        file="process.ini",
                        section="Debug Information",
                        line=50,
                    ),
                    # Test for ensuring invalid setting names are caught.
                    ValidationResult(
                        rule="NameViolation",
                        severity=Severity.WARNING,
                        message='The setting "InvalidSetting" is not a valid setting. Valid settings are: DebugLogFullParsingInfo, DebugLogFullExecutionInfo, DebugLogDetailBuiltInActions, ExpectLog, ConsoleOutput.',
                        file="process.ini",
                        section="Debug Information",
                        line=51,
                    ),
                    # Test for ensuring parse errors are caught.
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed correctly.",
                        file="process.ini",
                        section="Debug Information",
                        line=52,
                    ),
                    # Test reserved words used as condition names are caught.
                    ValidationResult(
                        rule="InvalidWordViolation",
                        severity=Severity.CRITICAL,
                        message='"debug" is a reserved word and cannot be used as a name in an assignment.',
                        file="process.ini",
                        section="Debug Information",
                        line=53,
                    ),
                    # Test for ensuring invalid setting names are caught.
                    ValidationResult(
                        rule="NameViolation",
                        severity=Severity.WARNING,
                        message='The setting "debug" is not a valid setting. Valid settings are: DebugLogFullParsingInfo, DebugLogFullExecutionInfo, DebugLogDetailBuiltInActions, ExpectLog, ConsoleOutput.',
                        file="process.ini",
                        section="Debug Information",
                        line=53,
                    ),
                ],
            ),
            (
                # Test to ensure that validation continues with a missing prompts file.
                "tests/data/debug-information-invalid-process.ini",
                None,
                [
                    ValidationResult(
                        rule="InformationOnly",
                        severity=Severity.INFO,
                        message="The prompts file was not supplied, therefore, assumptions have been made of boolean conditions. Transitions that rely on boolean conditions may not validate correctly.",
                        file="process.ini",
                    ),
                    ValidationResult(
                        rule="UnusedParameterViolation",
                        severity=Severity.WARNING,
                        message='The parameter "username" has been validated but is not used.',
                        file="process.ini",
                        section="CPM Parameters Validation",
                        line=30,
                    ),
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "ExpectLog" has been declared 2 times.',
                        file="process.ini",
                        section="Debug Information",
                    ),
                    # Test for ensuring blank values are caught when no = present
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.WARNING,
                        message='The value for "DebugLogFullParsingInfo" is blank. Setting should be explicitly set to "no".',
                        file="process.ini",
                        section="Debug Information",
                        line=44,
                    ),
                    # Test for ensuring blank values are caught when no = present
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.WARNING,
                        message='The value for "DebugLogFullExecutionInfo" is blank. Setting should be explicitly set to "no".',
                        file="process.ini",
                        section="Debug Information",
                        line=45,
                    ),
                    # Test for ensuring setting name case violation is caught.
                    ValidationResult(
                        rule="NameCaseViolation",
                        severity=Severity.WARNING,
                        message='The setting "expectlog" should be set as "ExpectLog".',
                        file="process.ini",
                        section="Debug Information",
                        line=48,
                    ),
                    # Test for ensuring setting value case violation is caught.
                    ValidationResult(
                        rule="ValueCaseViolation",
                        severity=Severity.WARNING,
                        message='The value for "expectlog" is set to "Yes" this should be in lower case.',
                        file="process.ini",
                        section="Debug Information",
                        line=48,
                    ),
                    # Test for ensuring logging is disabled.
                    ValidationResult(
                        rule="LoggingEnabledViolation",
                        severity=Severity.CRITICAL,
                        message='The value for "expectlog" is set to "Yes". It is recommended to set all settings in this section to "no" for production environments.',
                        file="process.ini",
                        section="Debug Information",
                        line=48,
                    ),
                    # Test for ensuring invalid setting values are caught.
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='The value for "ConsoleOutput" is set to "Maybe" and is invalid. Valid values are "no" and "yes".',
                        file="process.ini",
                        section="Debug Information",
                        line=49,
                    ),
                    # Test invalid token type in debug information section are caught.
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.CRITICAL,
                        message='The token type "Transition" is not valid in the "Debug Information" section.',
                        file="process.ini",
                        section="Debug Information",
                        line=50,
                    ),
                    # Test for ensuring invalid setting names are caught.
                    ValidationResult(
                        rule="NameViolation",
                        severity=Severity.WARNING,
                        message='The setting "InvalidSetting" is not a valid setting. Valid settings are: DebugLogFullParsingInfo, DebugLogFullExecutionInfo, DebugLogDetailBuiltInActions, ExpectLog, ConsoleOutput.',
                        file="process.ini",
                        section="Debug Information",
                        line=51,
                    ),
                    # Test for ensuring parse errors are caught.
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed correctly.",
                        file="process.ini",
                        section="Debug Information",
                        line=52,
                    ),
                    # Test reserved words used as condition names are caught.
                    ValidationResult(
                        rule="InvalidWordViolation",
                        severity=Severity.CRITICAL,
                        message='"debug" is a reserved word and cannot be used as a name in an assignment.',
                        file="process.ini",
                        section="Debug Information",
                        line=53,
                    ),
                    # Test for ensuring invalid setting names are caught.
                    ValidationResult(
                        rule="NameViolation",
                        severity=Severity.WARNING,
                        message='The setting "debug" is not a valid setting. Valid settings are: DebugLogFullParsingInfo, DebugLogFullExecutionInfo, DebugLogDetailBuiltInActions, ExpectLog, ConsoleOutput.',
                        file="process.ini",
                        section="Debug Information",
                        line=53,
                    ),
                ],
            ),
            (
                # Test to ensure that validation continues with a missing process file.
                "tests/data/valid-process.ini",
                None,
                [
                    ValidationResult(
                        rule="InformationOnly",
                        severity=Severity.INFO,
                        message="The prompts file was not supplied, therefore, assumptions have been made of boolean conditions. Transitions that rely on boolean conditions may not validate correctly.",
                        file="process.ini",
                    ),
                    ValidationResult(  # Valid as the username is used in the prompts file which is missing in this test.
                        rule="UnusedParameterViolation",
                        severity=Severity.WARNING,
                        message='The parameter "username" has been validated but is not used.',
                        file="process.ini",
                        section="CPM Parameters Validation",
                        line=30,
                    ),
                ],
            ),
            (
                # Test to ensure that validation continues with a missing prompts file.
                None,
                "tests/data/valid-prompts.ini",
                [],
            ),
        ],
    )
    def test_debug_information_section_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_violations: list[ValidationResult],
    ) -> None:
        """
        Tests for the debug information rule set.

        :param process_file: Path to the process file to use for the test case.
        :param prompts_file: Path to the prompts file to use for the test case.
        :param expected_violations: List of expected ValidationResult
        """
        validate = Validator.with_file(prompts_file_path=prompts_file, process_file_path=process_file)
        validate.validate()
        results = validate.get_violations()

        assert len(results) == len(expected_violations)

        for result in results:
            assert result in expected_violations

        assert validate.get_violations() == expected_violations
