"""Module for parsing prompts and process files."""
from collections import OrderedDict
from os.path import isfile

from tpc_plugin_validator.severity import Severity
from tpc_plugin_validator.prompts import Prompts
from tpc_plugin_validator.process import Process
from tpc_plugin_validator.validation_result import ValidationResult
from tpc_plugin_validator.ini_parser import IniParser


class Parser(object):

    __slots__ = (
        '_parsed',
        '_process',
        '_process_file_path',
        '_prompts',
        '_prompts_file_path',
        '_validations',
    )
    def __init__(self, prompts_file_path: str, process_file_path: str) -> None:
        """Initialize the Parser with file paths.

        :param prompts_file_path: Path to the prompt file.
        :param process_file_path: Path to the process file.
        """
        self._parsed = False
        self._process: Process | None = None
        self._process_file_path: str = process_file_path
        self._prompts: Prompts | None = None
        self._prompts_file_path: str = prompts_file_path
        self._validations: list[ValidationResult] = []

    def parse(self) -> None:
        """Parse the prompt and process files."""
        if self._parsed:
            return
        self._parse_prompt_file()
        self._parse_process_file()
        self._parsed = True

    def _parse_prompt_file(self) -> None:
        """
        Parse the prompt file and pop populate the Prompt dataclass.
        """
        parsed_prompts = self._parse_file(file_path=self._prompts_file_path)
        sections = parsed_prompts.keys()
        conditions_header = 'conditions'
        for section in sections:
            # Check for invalid sections.
            if section == 'default' and len(parsed_prompts[section]) == 0:
                continue
            if section == 'default' and len(parsed_prompts[section]) > 0:
                self._validations.append(
                    ValidationResult(
                        rule='ProcessFileContainsDefaultSection',
                        severity=Severity.WARNING,
                        message='The process file contains entries outwith the "conditions" section.',
                    )
                )
                continue
            # Only 'conditions' section is valid.
            if section.lower() != 'conditions':
                self._validations.append(
                    ValidationResult(
                        rule='ProcessInvalidSectionViolation',
                        severity=Severity.WARNING,
                        message=f'The process file contains an invalid section "{section}".',
                    )
                )
                continue
            # Check for section case violations.
            if section.lower() == 'conditions' and section.lower() != section:
                self._validations.append(
                    ValidationResult(
                        rule='ProcessSectionNameCaseViolation',
                        severity=Severity.WARNING,
                        message='The process "conditions" section should be lower case.',
                    )
                )
                conditions_header = section
        if 'conditions' not in [section.lower() for section in sections]:
            self._validations.append(
                ValidationResult(
                    rule='ProcessSectionMissingViolation',
                    severity=Severity.CRITICAL,
                    message='The process "conditions" section does not exist.',
                )
            )
            return

        conditions: dict[str, list[str]] = {}

        for line in parsed_prompts[conditions_header]:
            line_split = line.strip().split('=', maxsplit=1)
            key = line_split[0].strip()
            value = line_split[1].strip() or None
            if key not in conditions:
                conditions[key] = []
            conditions[key].append(value)

        self._prompts = Prompts(sections=list(sections), conditions=conditions)

    def _parse_process_file(self) -> None:
        """
        Parse the prompt file and populate the Process dataclass.
        """
        parsed_process = self._parse_file(self._process_file_path)
        #sections = parsed_process.sections()
        # TODO Fully implement process file parsing and validation.

    def _parse_file(self, file_path: str) -> dict[str, list[str]]:
        """
        Generic file parser to read the file ready for the specific file parser.

        :param file_path: Path to the file to be parsed.

        :raises FileNotFoundError: If the file does not exist.

        :return dict[str, list[str]]: Parsed file as a dictionary.
        """
        if not isfile(file_path):
            raise FileNotFoundError(f'The file at "{file_path}" does not exist or is not accessible.')

        ini_parser = IniParser()
        res = {}
        try:
            res = ini_parser.read(file_path)
        except FileNotFoundError:
            self._validations.append(
                ValidationResult(
                    rule='FILE_NOT_FOUND',
                    severity=Severity.CRITICAL,
                    message=f'The file at "{file_path}" does not exist or is not accessible.',
                )
            )
        return res

    @property
    def process(self) -> Process:
        """Get the parsed Process dataclass."""
        if not self._parsed or self._process is None:
            self.parse()
        return self._process

    @property
    def prompts(self) -> Prompts:
        """Get the parsed Prompts dataclass."""
        if not self._parsed or self._prompts is None:
            self.parse()
        return self._prompts

    @property
    def validations(self) -> list[ValidationResult]:
        """
        Get any validation errors.

        :return: List of validation results.
        """
        if not self._parsed:
            self.parse()
        return self._validations