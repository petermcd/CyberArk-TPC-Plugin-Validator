"""Tests for the process file rule set."""

import pytest

from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult
from tpc_plugin_validator.validator import Validator


class TestProcessFileRuleSet(object):
    """Tests for the process file rule set."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_violations",
        [
            (
                # Test to ensure that valid files produce no violations.
                "tests/data/process-file-invalid-process.ini",
                "tests/data/valid-prompts.ini",
                [
                    # Test to ensure invalid sections are caught.
                    ValidationResult(
                        rule="InvalidSectionNameViolation",
                        severity=Severity.WARNING,
                        message='The section "Dummy Section" has been declared but is an invalid section name.',
                        file="process.ini",
                    ),
                    # Test to ensure section name case issue is caught.
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "CPM Parameters Validation" has been declared as "cpm Parameters Validation".',
                        file="process.ini",
                        section="CPM Parameters Validation",
                    ),
                    # Test to ensure section name case issue is caught.
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "Debug Information" has been declared as "debug information".',
                        file="process.ini",
                        section="Debug Information",
                    ),
                    # Test invalid token type in process file default section is caught.
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.CRITICAL,
                        message='The token type "Transition" is not valid in the "default" section.',
                        file="process.ini",
                        section="default",
                        line=7,
                    ),
                    # Test for ensuring parse errors are caught.
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed correctly.",
                        file="process.ini",
                        section="default",
                        line=8,
                    ),
                    # Test to ensure section name case issue is caught.
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "parameters" has been declared as "Parameters".',
                        file="process.ini",
                        section="parameters",
                    ),
                    # Test to ensure section name case issue is caught.
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "transitions" has been declared as "Transitions".',
                        file="process.ini",
                        section="transitions",
                    ),
                ],
            ),
            (
                # Test to ensure that validation continues with a missing prompts file.
                "tests/data/process-file-invalid-process.ini",
                None,
                [
                    ValidationResult(
                        rule="InformationOnly",
                        severity=Severity.INFO,
                        message="The prompts file was not supplied, therefore, assumptions have been made of boolean conditions. Transitions that rely on boolean conditions may not validate correctly.",
                        file="process.ini",
                    ),
                    # Test to ensure invalid sections are caught.
                    ValidationResult(
                        rule="InvalidSectionNameViolation",
                        severity=Severity.WARNING,
                        message='The section "Dummy Section" has been declared but is an invalid section name.',
                        file="process.ini",
                    ),
                    # Test to ensure section name case issue is caught.
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "CPM Parameters Validation" has been declared as "cpm Parameters Validation".',
                        file="process.ini",
                        section="CPM Parameters Validation",
                    ),
                    ValidationResult(
                        rule="UnusedParameterViolation",
                        severity=Severity.WARNING,
                        message='The parameter "username" has been validated but is not used.',
                        file="process.ini",
                        section="CPM Parameters Validation",
                        line=34,
                    ),
                    # Test to ensure section name case issue is caught.
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "Debug Information" has been declared as "debug information".',
                        file="process.ini",
                        section="Debug Information",
                    ),
                    # Test invalid token type in process file default section is caught.
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.CRITICAL,
                        message='The token type "Transition" is not valid in the "default" section.',
                        file="process.ini",
                        section="default",
                        line=7,
                    ),
                    # Test for ensuring parse errors are caught.
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed correctly.",
                        file="process.ini",
                        section="default",
                        line=8,
                    ),
                    # Test to ensure section name case issue is caught.
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "parameters" has been declared as "Parameters".',
                        file="process.ini",
                        section="parameters",
                    ),
                    # Test to ensure section name case issue is caught.
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "transitions" has been declared as "Transitions".',
                        file="process.ini",
                        section="transitions",
                    ),
                ],
            ),
            (
                # Test to ensure that validation continues with a missing prompts file.
                "tests/data/valid-process.ini",
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
    def test_process_file_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_violations: list[ValidationResult],
    ) -> None:
        """
        Tests for the process file rule set.

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
