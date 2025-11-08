"""Tests for the states section rule set."""

import pytest

from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult
from tpc_plugin_validator.validator import Validator


class TestStatesSectionRuleSet(object):
    """Tests for the states section rule set."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_violations",
        [
            (
                # Test to ensure that valid files produce no violations.
                "tests/data/states-invalid-process.ini",
                "tests/data/states-invalid-prompts.ini",
                [
                    # Test for ensuring duplicate assignments are caught.
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "Wait" has been declared 2 times.',
                        file="process.ini",
                        section="states",
                    ),
                    # Test for ensuring invalid setting values are caught.
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.WARNING,
                        message='The code "1234" has been assigned to 2 different failure states.',
                        file="process.ini",
                        section="states",
                    ),
                    # Test to ensure declared states are used in transitions.
                    ValidationResult(
                        rule="UnusedStateViolation",
                        severity=Severity.WARNING,
                        message='The state "Source" has been declared but is not utilised in the transitions section.',
                        file="process.ini",
                        section="states",
                    ),
                    # Test reserved words used as condition names are caught.
                    ValidationResult(
                        rule="InvalidWordViolation",
                        severity=Severity.CRITICAL,
                        message='"Source" is a reserved word and cannot be used as a name in an assignment.',
                        file="process.ini",
                        section="states",
                        line=16,
                    ),
                    # Test for ensuring invalid setting values are caught.
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='The "END" state has been assigned the value "123", the "END" state should not have a value.',
                        file="process.ini",
                        section="states",
                        line=17,
                    ),
                    # Test for ensuring setting name case violation is caught.
                    ValidationResult(
                        rule="NameCaseViolation",
                        severity=Severity.CRITICAL,
                        message='The "END" state has been declared as "end", the "END" state should be in upper case.',
                        file="process.ini",
                        section="states",
                        line=17,
                    ),
                    # Test invalid token type in states section are caught.
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.CRITICAL,
                        message='The token type "Transition" is not valid in the "states" section.',
                        file="process.ini",
                        section="states",
                        line=18,
                    ),
                    # Test for ensuring parse errors are caught.
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed correctly.",
                        file="process.ini",
                        section="states",
                        line=19,
                    ),
                    # Test for ensuring invalid setting values are caught.
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='The fail state "SomeInvalidFailure" has an invalid failure code of "123", the failure code should be between 1000 and 9999.',
                        file="process.ini",
                        section="states",
                        line=23,
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
                # Test to ensure that validation continues with a missing process file.
                None,
                "tests/data/valid-prompts.ini",
                [],
            ),
        ],
    )
    def test_states_section_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_violations: list[ValidationResult],
    ) -> None:
        """
        Tests for the states section rule set.

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
