"""Base class for all file rule sets."""

from tpc_plugin_validator.rule_sets.rule_set import RuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import ValidSectionConfig, CONFIG_TYPE, FileNames, Violations


class FileRuleSet(RuleSet):
    _VALID_SECTIONS: dict[str, ValidSectionConfig] = {}

    def __init__(self, process_file, prompts_file, config: CONFIG_TYPE) -> None:
        """
        Initialize the file rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        :param config: Configuration.
        """
        super().__init__(prompts_file=prompts_file, process_file=process_file, config=config)

    def _validate_required_sections(self, file: FileNames) -> None:
        """
        Validate the required sections within the supplied file exist.

        :param file: The name of the file from the Filenames enum.
        """
        required_sections: list[str] = []
        required_sections.extend(
            required_section_name
            for required_section_name in self._VALID_SECTIONS
            if self._VALID_SECTIONS[required_section_name].get("required", False)
        )

        for required_section_name in required_sections:
            if not self._get_section_name(file=file, section_name=required_section_name):
                message: str = self._create_message(
                    message=f'"{required_section_name}" is a required section but this is missing',
                    file=file,
                    line_number=None,
                )
                self._add_violation(
                    name=Violations.missing_section_violation,
                    description=message,
                    severity=self._VALID_SECTIONS[required_section_name].get("severity_level", Severity.CRITICAL),
                )

    def _validate_sections(self, file: FileNames) -> None:
        """
        Validate the sections within the supplied file is correct.

        :param file: The name of the file from the Filenames enum.
        """

        valid_sections_dict: dict[str, str] = {
            valid_section_name.lower(): valid_section_name for valid_section_name in self._VALID_SECTIONS.keys()
        }
        for section_name in self._file_sections[file.value]:
            section = self._get_section_name(file=file, section_name=section_name)
            if section in self._VALID_SECTIONS.keys():
                continue
            elif section_name in valid_sections_dict:
                message: str = self._create_message(
                    message=f'The section "{valid_sections_dict[section_name]}" has been declared as "{section}"',
                    file=file,
                    line_number=None,
                )
                self._add_violation(
                    name=Violations.section_name_case_violation,
                    description=message,
                    severity=Severity.WARNING,
                )
            else:
                message = self._create_message(
                    message=f'Invalid section "{section}" identified',
                    file=file,
                    line_number=None,
                )
                self._add_violation(
                    name=Violations.invalid_section_name_violation,
                    description=message,
                    severity=Severity.WARNING,
                )
