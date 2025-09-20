"""Handle validation of the prompts file."""
from tpc_plugin_validator.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.file_rule_set import FileRuleSet
from tpc_plugin_validator.rule_sets.rule_set import FileNames
from tpc_plugin_validator.utilities.severity import Severity


class PromptsFileRuleSet(FileRuleSet):
    """
    Handle validation of the prompts file.

    Validation of individual section content is handled in their own rulesets.
    """

    _CONFIG_KEY: str = 'prompts'
    _FILE_TYPE: FileNames = FileNames.prompts
    _VALID_SECTIONS: dict[str, dict[str, bool | Severity]]  = {
        'conditions': {'required': True, 'severity_level': Severity.CRITICAL},
        'default': {'required': True, 'severity_level': Severity.CRITICAL},
    }
    _VALID_TOKENS: list[str] = [
        TokenName.COMMENT.value,
    ]

    def __init__(self, process_file, prompts_file, config: dict[str, dict[str, bool | int | str]]) -> None:
        """
        Initialize the prompts file rule set with prompts and process configurations.

        :param process_file: Parsed process file.
        :param prompts_file: Parsed prompts file.
        :param config: Not used, but included for interface consistency.
        """
        super().__init__(
            prompts_file=prompts_file,
            process_file=process_file,
            config=config
        )

    def validate(self) -> None:
        """Validate the prompts file."""
        self._validate_sections(file=self._FILE_TYPE)
        self._validate_required_sections(file=self._FILE_TYPE)
        self._validate_tokens(file=self._FILE_TYPE, section_override='default')
