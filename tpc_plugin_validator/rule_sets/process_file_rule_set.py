"""Handle validation of process file."""

from tpc_plugin_validator.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.file_rule_set import FileRuleSet
from tpc_plugin_validator.rule_sets.rule_set import FileNames
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.types import ValidSectionConfig, CONFIG_TYPE


class ProcessFileRuleSet(FileRuleSet):
    """
    Handle validation of the process file.

    Validation of individual section content is handled in their own rulesets.
    """

    _CONFIG_KEY: str = "process"
    _FILE_TYPE: FileNames = FileNames.process
    _VALID_SECTIONS: dict[str, ValidSectionConfig] = {
        "CPM Parameters Validation": {
            "required": True,
            "severity_level": Severity.WARNING,
        },
        "Debug Information": {"required": False, "severity_level": Severity.INFO},
        "default": {"required": True, "severity_level": Severity.CRITICAL},
        "parameters": {"required": False, "severity_level": Severity.INFO},
        "states": {"required": True, "severity_level": Severity.CRITICAL},
        "transitions": {"required": True, "severity_level": Severity.CRITICAL},
    }
    _VALID_TOKENS: list[str] = [
        TokenName.COMMENT.value,
    ]

    def __init__(self, process_file, prompts_file, config: CONFIG_TYPE) -> None:
        """
        Initialize the process file rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        :param config: Configuration.
        """
        super().__init__(prompts_file=prompts_file, process_file=process_file, config=config)

    def validate(self) -> None:
        """Validate the process file."""
        self._validate_sections(file=self._FILE_TYPE)
        self._validate_required_sections(file=self._FILE_TYPE)
        self._validate_tokens(file=self._FILE_TYPE, section_override="default")
