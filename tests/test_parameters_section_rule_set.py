"""Tests for the parameters section rule set."""

import pytest

from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult
from tpc_plugin_validator.validator import Validator


class TestParametersSectionRuleSet(object):
    """Tests for the parameters section rule set."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_results",
        [
            (
                "tests/data/parameter-invalid-process.ini",
                "tests/data/parameter-invalid-prompts.ini",
                [
                    # Test for ensuring invalid setting values are caught.
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='"SendHumanMin" is set to "twenty-two", the value must be numerical.',
                        file="process.ini",
                        section="parameters",
                        line=38,
                    ),
                    # Test for ensuring invalid setting values are caught.
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='"SendHumanMax" is set to "twenty-three", the value must be numerical.',
                        file="process.ini",
                        section="parameters",
                        line=39,
                    ),
                ],
            ),
            (
                "tests/data/parameter-invalid-process2.ini",
                "tests/data/parameter-invalid-prompts.ini",
                [
                    # Test for ensuring invalid setting values are caught.
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='"SendHumanMin" is set to -1.0 this cannot be less than 0.',
                        file="process.ini",
                        section="parameters",
                        line=38,
                    ),
                    # Test for ensuring invalid setting values are caught.
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='"SendHumanMax" is set to -1.0 this cannot be less than 0.',
                        file="process.ini",
                        section="parameters",
                        line=39,
                    ),
                ],
            ),
            (
                "tests/data/parameter-invalid-process3.ini",
                "tests/data/parameter-invalid-prompts.ini",
                [
                    # Test for ensuring duplicate assignments are caught.
                    ValidationResult(
                        rule="DuplicateAssignmentViolation",
                        severity=Severity.CRITICAL,
                        message='The assignment "PromptTimeout" has been declared 2 times.',
                        file="process.ini",
                        section="parameters",
                    ),
                    # Test for ensuring invalid setting values are caught.
                    ValidationResult(
                        rule="ValueViolation",
                        severity=Severity.CRITICAL,
                        message='"SendHumanMin" cannot be greater than "SendHumanMax", "SendHumanMin" is set to 4.0 and "SendHumanMax" is set to 2.0.',
                        file="process.ini",
                        section="parameters",
                        line=39,
                    ),
                    # Test invalid token type in parameters section are caught.
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.CRITICAL,
                        message='The token type "Transition" is not valid in the "parameters" section.',
                        file="process.ini",
                        section="parameters",
                        line=41,
                    ),
                    # Test reserved words used as condition names with differing case are caught.
                    ValidationResult(
                        rule="InvalidWordViolation",
                        severity=Severity.CRITICAL,
                        message='"open" is a reserved word and cannot be used as a name in an assignment.',
                        file="process.ini",
                        section="parameters",
                        line=42,
                    ),
                    # Test for ensuring parse errors are caught.
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed correctly.",
                        file="process.ini",
                        section="parameters",
                        line=43,
                    ),
                ],
            ),
        ],
    )
    def test_parameters_section_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_results: list[ValidationResult],
    ) -> None:
        """
        Tests for the parameters section rule set

        :param process_file: Path to the process file to use for the test case.
        :param prompts_file: Path to the prompts file to use for the test case.
        :param expected_results: List of expected ValidationResult
        """
        validate = Validator.with_file(prompts_file_path=prompts_file, process_file_path=process_file)
        validate.validate()
        results = validate.get_violations()

        assert len(results) == len(expected_results)

        for result in results:
            assert result in expected_results
