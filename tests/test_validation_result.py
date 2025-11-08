"""Tests for the ValidationResult object."""

import pytest

from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestTransitionsSectionRuleSet(object):
    """Tests for the ValidationResult object."""

    @pytest.mark.parametrize(
        "validation_result,expected_message",
        [
            (
                ValidationResult(
                    rule="InvalidTokenTypeViolation",
                    severity=Severity.CRITICAL,
                    message='The token type "Transition" is not valid in the "default" section.',
                    file="process.ini",
                    section="default",
                    line=7,
                ),
                'CRITICAL - process.ini:default(7) (InvalidTokenTypeViolation) The token type "Transition" is not valid in the "default" section.',
            ),
            (
                ValidationResult(
                    rule="SectionNameCaseViolation",
                    severity=Severity.WARNING,
                    message='The section "conditions" has been declared as "Conditions".',
                    file="prompts.ini",
                    section="conditions",
                ),
                'WARNING - prompts.ini:conditions (SectionNameCaseViolation) The section "conditions" has been declared as "Conditions".',
            ),
            (
                ValidationResult(
                    rule="InvalidSectionNameViolation",
                    severity=Severity.WARNING,
                    message='The section "Dummy Section" has been declared but is an invalid section name.',
                    file="process.ini",
                ),
                'WARNING - process.ini (InvalidSectionNameViolation) The section "Dummy Section" has been declared but is an invalid section name.',
            ),
            (
                ValidationResult(
                    rule="InvalidSectionNameViolation",
                    severity=Severity.INFO,
                    message='The section "Dummy Section" has been declared but is an invalid section name.',
                ),
                'INFO - (InvalidSectionNameViolation) The section "Dummy Section" has been declared but is an invalid section name.',
            ),
            (
                ValidationResult(
                    rule="InformationOnly",
                    severity=Severity.INFO,
                    message="The prompts file was not provided therefore validation rules requiring this file will be skipped.",
                ),
                "INFO - (InformationOnly) The prompts file was not provided therefore validation rules requiring this file will be skipped.",
            ),
        ],
    )
    def test_validation_result(self, validation_result: ValidationResult, expected_message: str) -> None:
        """
        Tests for the ValidationResult object.

        :param validation_result: Instance of ValidationResult object.
        :param expected_message: Expected message.
        """
        assert str(validation_result) == expected_message
