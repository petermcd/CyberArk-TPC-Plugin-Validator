"""Test the validator."""

import pytest

from tpc_plugin_validator.utilities.validation_result import ValidationResult
from tpc_plugin_validator.validator import Validator


class TestValidator(object):
    """Test the lexer."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,violations",
        [
            (
                "tests/data/valid-process.ini",
                "tests/data/valid-prompts.ini",
                [],
            )
        ],
    )
    def test_validator(self, process_file: str, prompts_file: str, violations: list[ValidationResult]) -> None:
        """
        Test to ensure that the validator works.

        :param process_file: Path to the process file to test.
        :param prompts_file: Path to the prompts file to test.
        :param violations: Expected violations.
        """
        with open(process_file, "r") as process_fh:
            process_file_content = process_fh.read()

        with open(prompts_file, "r") as prompts_fh:
            prompts_file_content = prompts_fh.read()

        validator = Validator(
            process_file_content=process_file_content, prompts_file_content=prompts_file_content, config={}
        )
        validator.validate()
        assert validator.get_violations() == violations

    @pytest.mark.parametrize(
        "process_file,prompts_file,violations",
        [
            (
                "tests/data/valid-process.ini",
                "tests/data/valid-prompts.ini",
                [],
            )
        ],
    )
    def test_validator_with_file_path(
        self, process_file: str, prompts_file: str, violations: list[ValidationResult]
    ) -> None:
        """
        Test to ensure that the validator works.

        :param process_file: Path to the process file to test.
        :param prompts_file: Path to the prompts file to test.
        :param violations: Expected violations.
        """

        validator = Validator.with_file(process_file_path=process_file, prompts_file_path=prompts_file, config={})
        validator.validate()
        assert validator.get_violations() == violations

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_message",
        [
            (
                "tests/data/doesnt_exist/process.ini",
                "tests/data/doesnt_exist/prompts.ini",
                "Process file not found: tests/data/doesnt_exist/process.ini",
            ),
            (
                "tests/data/doesnt_exist/process.ini",
                "tests/data/valid-prompts.ini",
                "Process file not found: tests/data/doesnt_exist/process.ini",
            ),
            (
                "tests/data/valid-process.ini",
                "tests/data/doesnt_exist/prompts.ini",
                "Process file not found: tests/data/doesnt_exist/prompts.ini",
            ),
        ],
    )
    def test_validator_with_file_path_exception(
        self, process_file: str, prompts_file: str, expected_message: str
    ) -> None:
        """
        Test to ensure that the validator works.

        :param process_file: Path to the process file to test.
        :param prompts_file: Path to the prompts file to test.
        :param expected_exception: Expected exception to be thrown.
        """
        with pytest.raises(FileNotFoundError) as excinfo:
            Validator.with_file(process_file_path=process_file, prompts_file_path=prompts_file, config={})

        assert excinfo.value.args[0] == expected_message
