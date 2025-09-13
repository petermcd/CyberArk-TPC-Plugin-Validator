"""Handle validation of parameters."""
from tpc_plugin_validator.lexer.tokens.assignment import Assignment
from tpc_plugin_validator.rule_sets.rule_set import RuleSet
from tpc_plugin_validator.utilities.severity import Severity


class Parameters(RuleSet):
    """Handle validation of parameters."""

    CONFIG_KEY: str = 'parameters'

    def validate(self) -> None:
        """Validate the settings in the process file."""
        if 'parameters' not in self._process_content.keys():
            self._add_violation(
                    name='ParametersNoParametersSectionViolation',
                    description='The process file does not contain a "parameters" section.',
                    severity=Severity.CRITICAL,
            )
            return

        parameters = self._process_content.get('parameters', [])

        human_max: Assignment | None = None
        human_min: Assignment | None = None

        for parameter in parameters:
            if not self._token_is_valid(token=parameter):
                self._add_violation(
                    name='ParametersTokenViolation',
                    description=f'The token type "{parameter.token_name}" is not valid in the "parameters" section, found on line {parameter.line_number}.',
                    severity=Severity.WARNING,
                )

            if parameter.token_name != 'Assignment':
                continue
            elif parameter.name == 'SendHumanMin':
                human_min = parameter
            elif parameter.name == 'SendHumanMax':
                human_max = parameter

        self._check_duplicates(
            tokens=self._process_content.get('parameters', []),
            rule_name='ParametersDuplicateParametersViolation',
            file_type='process'
        )

        self._check_human_min_max(human_min=human_min, human_max=human_max)

    def _check_human_min_max(self, human_min: Assignment | None, human_max: Assignment | None) -> None:
        """Check that the SendHumanMin and SendHumanMax have valid values if set."""

        if not human_min and not human_max:
            return

        try:
            if human_min and human_min.assigned and human_max and human_max.assigned and float(human_min.assigned) > float(human_max.assigned):
                self._add_violation(
                    name='ParametersMinGreaterThanMaxViolation',
                    severity=Severity.CRITICAL,
                    description=f'SendHumanMin is set to {float(human_min.assigned)} and SendHumanMax is set to {float(human_max.assigned)}, SendHumanMin cannot be greater than SendHumanMax.'
                )
        except ValueError:
            pass

        try:
            if human_min and human_min.assigned and float(human_min.assigned) < 0:
                self._add_violation(
                    name='ParametersMinLessThanZeroViolation',
                    severity=Severity.CRITICAL,
                    description=f'SendHumanMin is set to {float(human_min.assigned)} this cannot be less than 0.'
                )
        except ValueError:
            if human_min:
                self._add_violation(
                    name='ParametersMinInvalidValueViolation',
                    severity=Severity.CRITICAL,
                    description=f'SendHumanMin is set to "{human_min.assigned}", the value must be numerical, found on line {human_min.line_number}.'
                )

        try:
            if human_max and human_max.assigned and float(human_max.assigned) < 0:
                self._add_violation(
                    name='ParameterMaxLessThanZeroViolation',
                    severity=Severity.CRITICAL,
                    description=f'SendHumanMax is set to {float(human_max.assigned)} this cannot be less than 0.'
                )
        except ValueError:
            if human_max:
                self._add_violation(
                    name='ParametersMaxInvalidValueViolation',
                    severity=Severity.CRITICAL,
                    description=f'SendHumanMax is set to "{human_max.assigned}", the value must be numerical, found on line {human_max.line_number}.'
                )
