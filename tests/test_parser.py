"""Tests for the Parser class in tpc_plugin_validator.parser module."""
import pytest

from tpc_plugin_validator.parser import Parser
from tpc_plugin_validator.validation_result import ValidationResult


class TestParser(object):

    @pytest.mark.parametrize(
        'process_file, prompts_file, expected_results',
        [
            (
                'tests/data/OK-Process-Parses/process.ini',
                'tests/data/OK-Process-Parses/prompts.ini',
                [],
            ),
            (
                'tests/data/OK-Prompts-Parses/process.ini',
                'tests/data/OK-Prompts-Parses/prompts.ini',
                [],
            ),
        ]
    )
    def test_parser(self, process_file: str, prompts_file: str, expected_results: list[ValidationResult]) -> None:
        """
        Test the Parser class with various input files.

        :param process_file: Path to the process file.
        :param prompts_file: Path to the prompt file.
        :param expected_results: Expected validation results.
        """
        parser = Parser(prompts_file_path=prompts_file, process_file_path=process_file)
        parser.parse()
        assert parser._validations == expected_results

    @pytest.mark.parametrize(
        'process_file, prompts_file, expected_exception, expected_error',
        [
            (
                'tests/data/CRITICAL-Process-File-Doesnt-Exist/process.ini',
                'tests/data/CRITICAL-Process-File-Doesnt-Exist/prompts.ini',
                FileNotFoundError,
                'The file at "tests/data/CRITICAL-Process-File-Doesnt-Exist/process.ini" does not exist or is not accessible.',
            ),
            (
                'tests/data/CRITICAL-Prompts-File-Doesnt-Exist/process.ini',
                'tests/data/CRITICAL-Prompts-File-Doesnt-Exist/prompts.ini',
                FileNotFoundError,
                'The file at "tests/data/CRITICAL-Prompts-File-Doesnt-Exist/prompts.ini" does not exist or is not accessible.',
            ),
        ]
    )
    def test_parser_file_error(self, process_file: str, prompts_file: str, expected_exception: Exception, expected_error: str) -> None:
        """
        Test the Parser class with various input files that should raise errors.

        :param process_file: Path to the process file.
        :param prompts_file: Path to the prompt file.
        :param expected_exception: Expected exception type.
        :param expected_error: Expected error message.
        """
        parser = Parser(prompts_file_path=prompts_file, process_file_path=process_file)
        with pytest.raises(expected_exception) as excinfo:
            parser.parse()
        assert str(excinfo.value) == expected_error