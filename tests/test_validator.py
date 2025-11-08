"""Test the validator."""

import pytest

from tpc_plugin_validator.utilities.exceptions import ProgrammingError
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult
from tpc_plugin_validator.validator import Validator


class TestValidator(object):
    """Test the lexer."""

    @pytest.mark.parametrize(
        "process_file_path,prompts_file_path,violations",
        [
            (
                # Test to ensure that valid files produce no violations.
                "tests/data/valid-process.ini",
                "tests/data/valid-prompts.ini",
                [],
            ),
            (
                "tests/data/valid-process.ini",
                None,
                [
                    ValidationResult(
                        rule="InformationOnly",
                        severity=Severity.INFO,
                        message="The prompts file was not supplied, therefore, assumptions have been made of boolean conditions. Transitions that rely on boolean conditions may not validate correctly.",
                        file="process.ini",
                        section=None,
                        line=None,
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
                None,
                "tests/data/valid-prompts.ini",
                [],
            ),
        ],
    )
    def test_validator(
        self, process_file_path: str, prompts_file_path: str, violations: list[ValidationResult]
    ) -> None:
        """
        Test to ensure that the validator works.

        :param process_file_path: Path to the process file to test.
        :param prompts_file_path: Path to the prompts file to test.
        :param violations: Expected violations.
        """
        validator = Validator.with_file(process_file_path=process_file_path, prompts_file_path=prompts_file_path)
        validator.validate()
        assert validator.get_violations() == violations

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_violations",
        [
            (
                # Test to ensure that valid files produce no violations.
                "tests/data/valid-process.ini",
                "tests/data/valid-prompts.ini",
                [],
            ),
            (
                # Test to ensure that valid files produce no violations.
                "tests/data/valid-process-alt.ini",
                "tests/data/valid-prompts-alt.ini",
                [],
            ),
        ],
    )
    def test_validator_with_file_path(
        self,
        process_file: str,
        prompts_file: str,
        expected_violations: list[ValidationResult],
    ) -> None:
        """
        Test to ensure that the validator works.

        :param process_file: Path to the process file to test.
        :param prompts_file: Path to the prompts file to test.
        :param expected_violations: Expected violations.
        """
        validate = Validator.with_file(prompts_file_path=prompts_file, process_file_path=process_file)
        validate.validate()
        results = validate.get_violations()

        assert len(results) == len(expected_violations)

        for result in results:
            assert result in expected_violations

        assert validate.get_violations() == expected_violations

    @pytest.mark.parametrize(
        "process_file,prompts_file,exception_type,expected_message",
        [
            (
                "tests/data/doesnt_exist/process.ini",
                "tests/data/doesnt_exist/prompts.ini",
                FileNotFoundError,
                "The process file was not found: tests/data/doesnt_exist/process.ini",
            ),
            (
                "tests/data/doesnt_exist/process.ini",
                "tests/data/valid-prompts.ini",
                FileNotFoundError,
                "The process file was not found: tests/data/doesnt_exist/process.ini",
            ),
            (
                "tests/data/valid-process.ini",
                "tests/data/doesnt_exist/prompts.ini",
                FileNotFoundError,
                "The prompts file was not found: tests/data/doesnt_exist/prompts.ini",
            ),
            (
                None,
                None,
                ProgrammingError,
                "At least one of process file or prompts file required to complete validation.",
            ),
        ],
    )
    def test_validator_with_file_path_exception(
        self, process_file: str, prompts_file: str, exception_type, expected_message: str
    ) -> None:
        """
        Test to ensure that the validator works.

        :param process_file: Path to the process file to test.
        :param prompts_file: Path to the prompts file to test.
        :param expected_message: Expected message from the thrown exception.
        """
        with pytest.raises(exception_type) as excinfo:
            Validator.with_file(process_file_path=process_file, prompts_file_path=prompts_file)

        assert excinfo.value.args[0] == expected_message
