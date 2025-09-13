"""Handle validation of the parameter validations."""
from tpc_plugin_validator.lexer.tokens.parameter_validation import \
    ParameterValidation
from tpc_plugin_validator.rule_sets.rule_set import RuleSet
from tpc_plugin_validator.utilities.severity import Severity


class Parameter(RuleSet):
    """Handle validation of the parameter validations."""

    def validate(self) -> None:
        """Validate the parameter validations in the process file."""
        if 'CPM Parameters Validation' not in self._process_content.keys():
            self._add_violation(
                name='ParameterNoSectionViolation',
                description='The process file does not contain a "CPM Parameters Validation" section.',
                severity=Severity.WARNING,
            )
            return
        validation_tokens = self._process_content['CPM Parameters Validation']
        for validation_token in validation_tokens:
            if not self._token_is_valid(token=validation_token):
                self._add_violation(
                    name='ParameterTokenViolation',
                    description=f'The token type "{validation_token.token_name}" is not valid in the "CPM Parameters Validation" section, found on line {validation_token.line_number}.',
                    severity=Severity.WARNING,
                )
                continue
            if validation_token.token_name == 'Comment':
                continue
            if not self._check_parameter_name(token=validation_token):
                continue

    def _check_parameter_name(self, token: ParameterValidation):
        """
        Check to make sure the parameter is used.

        :param token: The token containing the parameter validation.
        """
        # TODO implement
        pass

    def _get_config_key(self) -> str:
        """
        Property to identify the config key to use for the rule set.

        :return: The config key as a string.
        """
        return 'parameter_validation'

    def _get_valid_token_types(self) -> set[str]:
        """
        Provide a set of token types allowed in the section being analysed.

        :return: Set of token types.
        """
        return {'Comment', 'Parameter Validation',}
