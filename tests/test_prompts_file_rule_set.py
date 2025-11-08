"""Tests for the prompts file rule set."""

import pytest

from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult
from tpc_plugin_validator.validator import Validator


class TestPromptsFileRuleSets(object):
    """Tests for the prompts file rule set."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_violations",
        [
            (
                # Test to ensure that valid files produce no violations.
                "tests/data/prompts-file-invalid-process.ini",
                "tests/data/prompts-file-invalid-prompts.ini",
                [
                    # Test to ensure section name case issue is caught.
                    ValidationResult(
                        rule="SectionNameCaseViolation",
                        severity=Severity.WARNING,
                        message='The section "conditions" has been declared as "Conditions".',
                        file="prompts.ini",
                        section="conditions",
                    ),
                    # Test invalid token type in prompts file default section are caught.
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.CRITICAL,
                        message='The token type "Transition" is not valid in the "default" section.',
                        file="prompts.ini",
                        section="default",
                        line=7,
                    ),
                    # Test for ensuring parse errors are caught.
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed correctly.",
                        file="prompts.ini",
                        section="default",
                        line=8,
                    ),
                ],
            ),
            (
                "tests/data/valid-process.ini",
                "tests/data/empty-prompts.ini",
                [
                    # Expected failure as no conditions section exists.
                    ValidationResult(
                        rule="UnusedParameterViolation",
                        severity=Severity.WARNING,
                        message='The parameter "username" has been validated but is not used.',
                        file="process.ini",
                        section="CPM Parameters Validation",
                        line=30,
                    ),
                    # Expected failure as no conditions section exists.
                    ValidationResult(
                        rule="InvalidConditionViolation",
                        severity=Severity.CRITICAL,
                        message='The condition "Hello" used in the transition from "Init" to "Wait" but has not been declared.',
                        file="process.ini",
                        section="transitions",
                        line=21,
                    ),
                    # Expected failure as no conditions section exists.
                    ValidationResult(
                        rule="InvalidConditionViolation",
                        severity=Severity.CRITICAL,
                        message='The condition "Waiting" used in the transition from "Wait" to "IsWaiting" but has not been declared.',
                        file="process.ini",
                        section="transitions",
                        line=22,
                    ),
                    # Expected failure as no conditions section exists.
                    ValidationResult(
                        rule="InvalidConditionViolation",
                        severity=Severity.CRITICAL,
                        message='The condition "TRUE" used in the transition from "IsWaiting" to "SetPassword" but has not been declared.',
                        file="process.ini",
                        section="transitions",
                        line=23,
                    ),
                    # Expected failure as no conditions section exists.
                    ValidationResult(
                        rule="InvalidConditionViolation",
                        severity=Severity.CRITICAL,
                        message='The condition "Failure" used in the transition from "Wait" to "SomeFailure" but has not been declared.',
                        file="process.ini",
                        section="transitions",
                        line=24,
                    ),
                    # Expected failure as no conditions section exists.
                    ValidationResult(
                        rule="InvalidConditionViolation",
                        severity=Severity.CRITICAL,
                        message='The condition "Goodbye" used in the transition from "SetPassword" to "END" but has not been declared.',
                        file="process.ini",
                        section="transitions",
                        line=25,
                    ),
                    # Test to ensure missing section is captured.
                    ValidationResult(
                        rule="MissingSectionViolation",
                        severity=Severity.CRITICAL,
                        message='"conditions" is a required section but has not been declared.',
                        file="prompts.ini",
                        section="conditions",
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
                    # Expected failure as no conditions section exists.
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
                # Test to ensure that validation continues with a missing process file.
                None,
                "tests/data/valid-prompts.ini",
                [],
            ),
        ],
    )
    def test_prompts_file_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_violations: list[ValidationResult],
    ) -> None:
        """
        Tests for the prompts file rule set.

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
