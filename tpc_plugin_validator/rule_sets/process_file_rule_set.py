"""Handle validation of a process file."""

from typing import ClassVar

from tpc_plugin_parser.lexer.utilities.token_name import TokenName

from tpc_plugin_validator.rule_sets.file_rule_set import FileRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import FileNames, SectionNames, ValidSectionConfig


class ProcessFileRuleSet(FileRuleSet):
    """
    Handle validation of the process file.

    Validation of individual section content is handled in their own rulesets.
    """

    _CONFIG_KEY: ClassVar[str] = "process"
    _FILE_TYPE: ClassVar[FileNames] = FileNames.process
    _VALID_SECTIONS: ClassVar[dict[str, ValidSectionConfig]] = {
        SectionNames.cpm_parameters_validation.value: {
            "required": True,
            "severity_level": Severity.WARNING,
        },
        SectionNames.debug_information.value: {"required": False, "severity_level": Severity.INFO},
        SectionNames.default.value: {"required": True, "severity_level": Severity.CRITICAL},
        SectionNames.parameters.value: {"required": False, "severity_level": Severity.INFO},
        SectionNames.states.value: {"required": True, "severity_level": Severity.CRITICAL},
        SectionNames.transitions.value: {"required": True, "severity_level": Severity.CRITICAL},
    }
    _VALID_TOKENS: ClassVar[list[str]] = [
        TokenName.COMMENT.value,
    ]

    def validate(self) -> None:
        """Validate the process file."""
        if not self.has_process_file:
            # Skip as we were not supplied the required process file.
            return

        self._validate_sections(file=self._FILE_TYPE)
        self._validate_required_sections(file=self._FILE_TYPE)
        self._validate_tokens(file=self._FILE_TYPE, section_override=SectionNames.default)
