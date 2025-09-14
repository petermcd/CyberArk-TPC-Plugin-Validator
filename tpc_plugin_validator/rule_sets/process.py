"""Handle validation of the process file."""
from tpc_plugin_validator.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.rule_set import RuleSet
from tpc_plugin_validator.utilities.severity import Severity


class Process(RuleSet):
    """Handle validation of the process file."""

    CONFIG_KEY: str = 'process'

    def validate(self) -> None:
        """Validate the sections and default section in the process file."""
        self._check_valid_sections()
        self._check_default()

    def _check_default(self):
        """Check to ensure the default section of the process file is blank or only contains comments."""
        for default_item in self._process_content.get('default', []):
            if default_item.token_name != TokenName.COMMENT.value:
                self._add_violation(
                    name='ProcessDefaultContentViolation',
                    description=f'A token of type "{default_item.token_name}" has been found in the process file outwith a valid section on line {default_item.line_number}.',
                    severity=Severity.WARNING,
                )

    def _check_valid_sections(self):
        """Check to ensure only valid sections are found the process file."""
        # This check ignores case, case-sensitive checks are carried out elsewhere.
        allowed_sections = (
            'cpm parameters validation',
            'debug information',
            'default',
            'parameters',
            'states',
            'transitions',
        )
        for section_name in self._process_content.keys():
            if section_name.lower() not in allowed_sections:
                self._add_violation(
                    name='ProcessInvalidSectionViolation',
                    description=f'An invalid section "{section_name}" has been found in the process file.',
                    severity=Severity.WARNING,
                )
