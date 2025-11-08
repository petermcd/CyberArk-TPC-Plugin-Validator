"""Handle validation of the prompts file."""

from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.file_rule_set import FileRuleSet
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import ValidSectionConfig, FileNames, SectionNames


class PromptsFileRuleSet(FileRuleSet):
    """
    Handle validation of the prompts file.

    Validation of individual section content is handled in their own rulesets.
    """

    _CONFIG_KEY: str = "prompts"
    _FILE_TYPE: FileNames = FileNames.prompts
    _VALID_SECTIONS: dict[str, ValidSectionConfig] = {
        SectionNames.conditions.value: {"required": True, "severity_level": Severity.CRITICAL},
        SectionNames.default.value: {"required": True, "severity_level": Severity.CRITICAL},
    }
    _VALID_TOKENS: list[str] = [
        TokenName.COMMENT.value,
    ]

    def validate(self) -> None:
        """Validate the prompts file."""
        if not self.has_prompts_file:
            # Skip as we were not supplied the required process file.
            return

        self._validate_sections(file=self._FILE_TYPE)
        self._validate_required_sections(file=self._FILE_TYPE)
        self._validate_tokens(file=self._FILE_TYPE, section_override=SectionNames.default)
