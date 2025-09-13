"""Handle validation of the parameter validations."""
from tpc_plugin_validator.lexer.tokens.cpm_parameter_validation import \
    CPMParameterValidation
from tpc_plugin_validator.lexer.utilities.token_name import TokenName
from tpc_plugin_validator.rule_sets.rule_set import RuleSet
from tpc_plugin_validator.utilities.severity import Severity


class CPMParameter(RuleSet):
    """Handle validation of the parameter validations."""

    CONFIG_KEY='cpm_parameter_validation'
    VALID_TOKEN_TYPES={TokenName.COMMENT.value, TokenName.CPM_PARAMETER_VALIDATION.value,}

    def validate(self) -> None:
        """Validate the parameter validations in the process file."""
        if 'CPM Parameters Validation' not in self._process_content.keys():
            self._add_violation(
                name='CPMParameterNoSectionViolation',
                description='The process file does not contain a "CPM Parameters Validation" section.',
                severity=Severity.WARNING,
            )
            return
        validation_tokens = self._process_content['CPM Parameters Validation']
        for validation_token in validation_tokens:
            if not self._token_is_valid(token=validation_token):
                self._add_violation(
                    name='CPMParameterTokenViolation',
                    description=f'The token type "{validation_token.token_name}" is not valid in the "CPM Parameters Validation" section, found on line {validation_token.line_number}.',
                    severity=Severity.WARNING,
                )
                continue
            if validation_token.token_name == 'Comment':
                continue
            if not self._check_parameter_usage(token=validation_token):
                continue

    def _check_parameter_usage(self, token: CPMParameterValidation):
        """
        Check to make sure the parameter is used.

        :param token: The token containing the parameter validation.
        """
        if token.token_name != 'CPM Parameter Validation':
            return

        allowed_missing: set[str] = {
            'ProcessFileName',
            'PromptsFileName',
        }

        if token.name in allowed_missing:
            return

        for condition in self._prompts_content.get('conditions', []):
            if condition.token_name != 'Assignment':
                continue
            if condition.assigned and f'<{token.name}>' in condition.assigned:
                return

        for state in self._process_content.get('states', []):
            if state.token_name != 'Assignment':
                continue
            if state.assigned and f'<{token.name}>' in state.assigned:
                return

        self._add_violation(
            name='CPMParameterUnusedParameterViolation',
            description=f'The parameter "{token.name}" is validated but is not used, found on line {token.line_number}.',
            severity=Severity.WARNING,
        )
