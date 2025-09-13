"""Handle validation of parameters."""
from tpc_plugin_validator.rule_sets.rule_set import RuleSet
from tpc_plugin_validator.utilities.severity import Severity


class Parameters(RuleSet):
    """Handle validation of parameters."""

    CONFIG_KEY='parameters'

    def validate(self) -> None:
        """Validate the settings in the process file."""
        if 'parameters' not in self._process_content.keys():
            self._add_violation(
                    name='ParametersNoParametersSectionViolation',
                    description='The process file does not contain a "parameters" section.',
                    severity=Severity.CRITICAL,
            )
            return

        parameters = self._prompts_content.get('parameters', [])
        for parameter in parameters:
            if not self._token_is_valid(token=parameter):
                self._add_violation(
                    name='ParametersTokenViolation',
                    description=f'The token type "{parameter.token_name}" is not valid in the "condition" section, found on line {parameter.line_number}.',
                    severity=Severity.WARNING,
                )

        self._check_duplicates(
            tokens=self._process_content.get('parameters', []),
            rule_name='ParametersDuplicateParametersViolation',
            file_type='process'
        )

        self._check_human_min_max()

    def _check_human_min_max(self) -> None:
        """Check that the SendHumanMin and SendHumanMax have valid values if set."""
        human_min: float | None = None
        human_max: float | None = None

        for token in self._process_content.get('parameters', []):
            if token.token_name != 'Assignment':
                continue
            if token.name == 'SendHumanMin':
                human_min = float(token.assigned)
                continue
            if token.name == 'SendHumanMax':
                human_max = float(token.assigned)

        if human_min is not None and human_max is not None and human_min > human_max:
            self._add_violation(
                name='ParameterMinGreaterThanMaxViolation',
                severity=Severity.CRITICAL,
                description=f'SendHumanMin is set to {human_min} and SendHumanMax is set to {human_max}, SendHumanMin cannot be greater than SendHumanMax.'
            )

        if human_min is not None and human_min < 0:
            self._add_violation(
                name='ParameterMinLessThanZeroViolation',
                severity=Severity.CRITICAL,
                description=f'SendHumanMin is set to {human_min} this cannot be less than 0.'
            )

        if human_max is not None and human_max < 0:
            self._add_violation(
                name='ParameterMaxLessThanZeroViolation',
                severity=Severity.CRITICAL,
                description=f'SendHumanMax is set to {human_max} this cannot be less than 0.'
            )
