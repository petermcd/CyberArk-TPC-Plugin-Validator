"""Handle validation of the prompts file."""
from collections import Counter

from tpc_plugin_validator.rule_sets.rule_set import RuleSet
from tpc_plugin_validator.utilities.severity import Severity


class Prompts(RuleSet):
    """ Validate the logging settings in the process file. """

    def validate(self) -> None:
        """Validate the prompts in the prompts file."""
        self._check_valid_sections()
        self._check_default()
        if 'conditions' not in self._prompts_content.keys():
            self._add_violation(
                    name='PromptsNoConditionSectionViolation',
                    description='The prompts file does not contain a "conditions" section, therefore, the plugin cannot transitions between states.',
                    severity=Severity.CRITICAL,
            )
            return
        conditions = self._prompts_content.get('conditions', {})
        for condition in conditions:
            if not self._token_is_valid(token=condition):
                self._add_violation(
                    name='PromptsConditionTokenViolation',
                    description=f'The token type "{condition.token_name}" is not valid in the "condition" section, found on line {condition.line_number}.',
                    severity=Severity.WARNING,
                )
                continue
            if condition.token_name == 'Comment':
                continue
            if not self._check_condition_used(token=condition):
                self._add_violation(
                    name='PromptsUnusedConditionViolation',
                    description=f'The condition "{condition.name}" is declared in the prompts file on line {condition.line_number} but is not used in the process file.',
                    severity=Severity.WARNING,
                )

        self._check_duplicates()

    def _check_condition_used(self, token) -> bool:
        """
        Check to ensure all conditions are used

        :param token: The token to check.

        :return: True if used, Otherwise False.
        """
        for transition in self._process_content.get('transitions', {}):
            if transition.token_name != 'State Transition':
                continue
            if token.name == transition.condition:
                return True
        return False

    def _check_default(self):
        """Check to ensure the default section of the prompt file is blank or only contains comments."""
        for default_item in self._prompts_content.get('default', []):
            if default_item.token_name != 'Comment':
                self._add_violation(
                    name='PromptsDefaultContentViolation',
                    description=f'A token of type "{default_item.token_name}" has been found in the prompt file outwith a valid section on line {default_item.line_number}.',
                    severity=Severity.WARNING,
                )

    def _check_duplicates(self):
        """Check to ensure all conditions are used"""
        conditions = self._prompts_content.get('conditions', {})
        condition_keys = []
        condition_keys.extend(condition.name for condition in conditions if condition.token_name == 'Assignment')
        counted_keys = Counter(condition_keys)
        for condition_name in counted_keys:
            if counted_keys[condition_name] > 1:
                self._add_violation(
                    name='PromptsDuplicateConditionViolation',
                    description=f'The condition "{condition_name}" has been declared {counted_keys[condition_name]} times in the process file.',
                    severity=Severity.WARNING,
                )

    def _check_valid_sections(self):
        """Check to ensure only valid sections are found the prompt file."""
        allowed_sections = ('default', 'conditions')
        for section_name in self._prompts_content.keys():
            if section_name not in allowed_sections:
                self._add_violation(
                    name='PromptsInvalidSectionViolation',
                    description=f'An invalid section "{section_name}" has been found in the prompt file.',
                    severity=Severity.WARNING,
                )

    def _get_config_key(self) -> str:
        """
        Property to identify the config key to use for the rule set.

        :return: The config key as a string.
        """
        return 'prompts'

    def _get_valid_token_types(self) -> set[str]:
        """
        Provide a set of token types allowed in the section being analysed.

        :return: Set of token types.
        """
        return {'Assignment', 'Comment',}
