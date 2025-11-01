"""Abstract class for all rule sets."""

from abc import ABC

from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.utilities.exceptions import ProgrammingError
from tpc_plugin_validator.utilities.invalid_words import INVALID_WORDS
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import CONFIG_TYPE, FileNames, SectionNames, Violations
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class RuleSet(ABC):
    __slots__ = (
        '_config',
        '_file_sections',
        '_process_file',
        '_prompts_file',
        '_violations',
    )

    _CONFIG_KEY: str = ''
    _FILE_TYPE: FileNames = FileNames.prompts
    _SECTION_NAME: SectionNames = SectionNames.default
    _VALID_TOKENS: list[str] = []

    def __init__(self, process_file, prompts_file, config: CONFIG_TYPE) -> None:
        """
        Initialize the rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        :param config: Configuration.
        """
        self._config = config.get(self._CONFIG_KEY, {})
        self._file_sections: dict[str, dict[str, str]] = {}
        self._process_file = process_file
        self._prompts_file = prompts_file
        self._violations: list[ValidationResult] = []

        self._extract_sections()

    def get_violations(self) -> list[ValidationResult]:
        """
        Getter for the violations.

        :return: List of ValidationResult
        """
        return self._violations

    def _add_violation(
        self,
        name: Violations,
        severity: Severity,
        message: str,
        file: FileNames | str | None = None,
        section: SectionNames | str | None = None,
        line: int | None = None,
    ) -> None:
        """
        Add a new violation.

        :param name: The name of the violation.
        :param message: The text describing the violation.
        :param severity: The severity of the violation.
        """
        if isinstance(file, FileNames):
            file = file.value
        if isinstance(section, SectionNames):
            section = section.value

        self._violations.append(
            ValidationResult(
                rule=name.value,
                severity=severity,
                message=message,
                file=str(file) if file else None,
                section=str(section) if section else None,
                line=line,
            )
        )

    def _extract_sections(self) -> None:
        """Create a dictionary of section names so that we can work regardless of case."""
        self._file_sections = {
            str(FileNames.process.value): {},
            str(FileNames.prompts.value): {},
        }
        for section in self._process_file.keys():
            self._file_sections[FileNames.process.value][section.lower()] = section
        for section in self._prompts_file.keys():
            self._file_sections[FileNames.prompts.value][section.lower()] = section

    def _get_section(self, file: FileNames, section_name: SectionNames):
        """
        Fetch the specified section from the specified file.

        :param file: The name of the file from the Filenames enum.
        :param section_name: Section to fetch.

        :raises ProgrammingError: If an invalid file is given.

        :return: The section requested.
        """
        if file.value == FileNames.process.value:
            fetch_from = self._process_file
        elif file.value == FileNames.prompts.value:
            fetch_from = self._prompts_file
        else:
            raise ProgrammingError(f'Invalid file name provided to _get_section in {type(self).__name__}.')

        section_name_fetched = self._file_sections[file.value].get(section_name.value.lower(), None)
        return fetch_from.get(section_name_fetched, None) if section_name_fetched else None

    def _get_section_name(self, file: FileNames, section_name: str) -> str | None:
        """
        Fetch the section name as it was specified in the given file.

        :param file: The name of the file from the Filenames enum.
        :param section_name: The section name we require.

        :return: The section name as it was provided in the file.
        """
        return self._file_sections[file.value].get(section_name.lower(), None)

    def _validate_tokens(self, file: FileNames, section_override: SectionNames | None = None) -> None:
        """
        Validate the token types against _VALID_TOKENS in the section.

        :param file: The name of the file from the Filenames enum.
        :param section_override: The section to analyze if not self._SECTION_NAME.
        """

        required_section = section_override or self._SECTION_NAME

        section = self._get_section(file=file, section_name=required_section)

        if not section:
            return

        for token in section:
            if token.token_name == TokenName.PARSE_ERROR.value:
                self._add_violation(
                    name=Violations.parse_error_violation,
                    severity=Severity.CRITICAL,
                    message='Line could not be parsed correctly.',
                    file=file,
                    section=required_section,
                    line=token.line_number,
                )
                continue

            if token.token_name == TokenName.ASSIGNMENT.value and token.name.lower() in INVALID_WORDS:
                self._add_violation(
                    name=Violations.invalid_word_violation,
                    severity=Severity.CRITICAL,
                    message=f'"{token.name}" is a reserved word and cannot be used as a name in an assignment.',
                    file=file,
                    section=required_section,
                    line=token.line_number,
                )

            if token.token_name not in self._VALID_TOKENS:
                self._add_violation(
                    name=Violations.invalid_token_type_violation,
                    severity=Severity.WARNING,
                    message=f'The token type "{token.token_name}" is not valid in the "{required_section.value}" section.',
                    file=file,
                    section=required_section,
                    line=token.line_number,
                )
