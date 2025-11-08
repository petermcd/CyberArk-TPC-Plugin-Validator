"""Tests for the conditions section rule set."""

import pytest

from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult
from tpc_plugin_validator.validator import Validator


class TestConditionsSectionRuleSet(object):
    """Tests for the debug information rule set."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_violations",
        [
            (
                "tests/data/conditions-invalid-process.ini",
                "tests/data/conditions-invalid-prompts.ini",
                [
                    # Test for ensuring duplicate assignments are caught.
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "Goodbye" has been declared 3 times.',
                        file="prompts.ini",
                        section="conditions",
                    ),
                    # Test reserved words used as condition names are caught.
                    ValidationResult(
                        rule="InvalidWordViolation",
                        severity=Severity.CRITICAL,
                        message='"sQl" is a reserved word and cannot be used as a name in an assignment.',
                        file="prompts.ini",
                        section="conditions",
                        line=11,
                    ),
                    # Test reserved word used as condition name with differing case.
                    ValidationResult(
                        rule="UnusedConditionViolation",
                        severity=Severity.WARNING,
                        message='The condition "sQl" is declared but is not used.',
                        file="prompts.ini",
                        section="conditions",
                        line=11,
                    ),
                    # Test for conditions declared but unused.
                    ValidationResult(
                        rule="UnusedConditionViolation",
                        severity=Severity.WARNING,
                        message='The condition "Unused" is declared but is not used.',
                        file="prompts.ini",
                        section="conditions",
                        line=17,
                    ),
                    # Test invalid token type in conditions section are caught.
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.CRITICAL,
                        message='The token type "Transition" is not valid in the "conditions" section.',
                        file="prompts.ini",
                        section="conditions",
                        line=20,
                    ),
                    # Test reserved words used as condition names are caught.
                    ValidationResult(
                        rule="InvalidWordViolation",
                        severity=Severity.CRITICAL,
                        message='"CD" is a reserved word and cannot be used as a name in an assignment.',
                        file="prompts.ini",
                        section="conditions",
                        line=21,
                    ),
                    # Test reserved words used as condition names are caught.
                    ValidationResult(
                        rule="UnusedConditionViolation",
                        severity=Severity.WARNING,
                        message='The condition "CD" is declared but is not used.',
                        file="prompts.ini",
                        section="conditions",
                        line=21,
                    ),
                    # Test for ensuring parse errors are caught.
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed correctly.",
                        file="prompts.ini",
                        section="conditions",
                        line=22,
                    ),
                ],
            ),
        ],
    )
    def test_conditions_section_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_violations: list[ValidationResult],
    ) -> None:
        """
        Tests for the conditions section rule set.

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
