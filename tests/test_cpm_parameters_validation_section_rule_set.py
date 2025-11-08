"""Tests for the CPM Parameters Validation section rule set."""

import pytest

from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult
from tpc_plugin_validator.validator import Validator


class TestCPMParametersValidationSectionRuleSet(object):
    """Tests for the CPM Parameters Validation section rule set."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_violations",
        [
            (
                # Test to ensure that valid files produce no violations.
                "tests/data/cpm-parameters-validation-invalid-process.ini",
                "tests/data/cpm-parameters-validation-invalid-prompts.ini",
                [
                    # Test for ensuring duplicate assignments are caught.
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "password" has been declared 2 times.',
                        file="process.ini",
                        section="CPM Parameters Validation",
                    ),
                    # Test to catch parameters validated but not used.
                    ValidationResult(
                        rule="UnusedParameterViolation",
                        severity=Severity.WARNING,
                        message='The parameter "username" has been validated but is not used.',
                        file="process.ini",
                        section="CPM Parameters Validation",
                        line=30,
                    ),
                    # Test invalid token type in cpm parameters validations section are caught.
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.CRITICAL,
                        message='The token type "Transition" is not valid in the "CPM Parameters Validation" section.',
                        file="process.ini",
                        section="CPM Parameters Validation",
                        line=33,
                    ),
                    # Test for ensuring parse errors are caught.
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed correctly.",
                        file="process.ini",
                        section="CPM Parameters Validation",
                        line=35,
                    ),
                ],
            ),
            (
                # Test to ensure that validation continues with a missing prompts file.
                "tests/data/cpm-parameters-validation-invalid-process.ini",
                None,
                [
                    ValidationResult(
                        rule="InformationOnly",
                        severity=Severity.INFO,
                        message="The prompts file was not supplied, therefore, assumptions have been made of boolean conditions. Transitions that rely on boolean conditions may not validate correctly.",
                        file="process.ini",
                    ),
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "password" has been declared 2 times.',
                        file="process.ini",
                        section="CPM Parameters Validation",
                    ),
                    # Test to catch parameters validated but not used.
                    ValidationResult(
                        rule="UnusedParameterViolation",
                        severity=Severity.WARNING,
                        message='The parameter "username" has been validated but is not used.',
                        file="process.ini",
                        section="CPM Parameters Validation",
                        line=30,
                    ),
                    # Test invalid token type in cpm parameters validations section are caught.
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.CRITICAL,
                        message='The token type "Transition" is not valid in the "CPM Parameters Validation" section.',
                        file="process.ini",
                        section="CPM Parameters Validation",
                        line=33,
                    ),
                    # Test for ensuring parse errors are caught.
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed correctly.",
                        file="process.ini",
                        section="CPM Parameters Validation",
                        line=35,
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
    def test_cpm_parameters_validation_section_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_violations: list[ValidationResult],
    ) -> None:
        """
        Tests for the CPM Parameters Validation section rule set.

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
