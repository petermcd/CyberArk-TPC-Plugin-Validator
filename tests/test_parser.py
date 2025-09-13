"""Tests for the Parser class in tpc_plugin_validator.parser module."""
import pytest

from tpc_plugin_validator.parser.parser import Parser


class TestParser(object):
    """Test for the Parser class."""

    @pytest.mark.parametrize(
        'process_file,prompts_file,expected_error',
        [
            (
                'tests/data/CRITICAL-Process-File-Doesnt-Exist/process.ini',
                'tests/data/CRITICAL-Process-File-Doesnt-Exist/prompts.ini',
                'The process file "tests/data/CRITICAL-Process-File-Doesnt-Exist/process.ini" does not exist or is not accessible.',
            ),
            (
                'tests/data/CRITICAL-Prompts-File-Doesnt-Exist/process.ini',
                'tests/data/CRITICAL-Prompts-File-Doesnt-Exist/prompts.ini',
                'The prompts file "tests/data/CRITICAL-Prompts-File-Doesnt-Exist/prompts.ini" does not exist or is not accessible.',
            ),
        ]
    )
    def test_parser_file_error(self, process_file: str, prompts_file: str, expected_error: str) -> None:
        """
        Test the Parser class with various input files that should raise errors.

        :param process_file: Path to the process file.
        :param prompts_file: Path to the prompt file.
        :param expected_error: Expected error message.
        """
        with pytest.raises(FileNotFoundError, match=expected_error):
            Parser(prompts_file=prompts_file, process_file=process_file)
