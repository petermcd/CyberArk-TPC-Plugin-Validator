"""Test states rule sets."""
import pytest

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.states import States
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestStatesRuleSets(object):
    """Test states rule sets."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_results",
        [
            (
                'tests/data/CRITICAL-StatesNoStatesSectionViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='StatesNoStatesSectionViolation',
                        severity=Severity.CRITICAL,
                        message='The process file does not contain a "states" section.'
                    ),
                ],
            ),
            (
                'tests/data/WARNING-StatesTokenViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='StatesTokenViolation',
                        severity=Severity.WARNING,
                        message='The token type "State Transition" is not valid in the "states" section, found on line 10.'
                    ),
                ],
            ),
            (
                'tests/data/CRITICAL-StatesEndStateCaseViolation-NoValue/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='StatesEndStateCaseViolation',
                        severity=Severity.CRITICAL,
                        message='The END state has been declared as "end", the END state should be in upper case, found on line 8.'
                    ),
                ],
            ),
            (
                'tests/data/CRITICAL-StatesEndStateCaseViolation-WithValue/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='StatesEndStateCaseViolation',
                        severity=Severity.CRITICAL,
                        message='The END state has been declared as "end", the END state should be in upper case, found on line 8.'
                    ),
                    ValidationResult(
                        rule='StatesEndStateValueViolation',
                        severity=Severity.CRITICAL,
                        message='The END state has been assigned the value "dummy", the END state should not have a value, found on line 8.'
                    ),
                ],
            ),
            (
                'tests/data/OK-States/process.ini',
                'tests/data/empty_prompts.ini',
                [],
            ),
            (
                'tests/data/CRITICAL-StatesEndStateValueViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='StatesEndStateValueViolation',
                        severity=Severity.CRITICAL,
                        message='The END state has been assigned the value "dummy", the END state should not have a value, found on line 8.'
                    ),
                ],
            ),
            (
                'tests/data/CRITICAL-StatesFailStateViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='StatesFailStateViolation',
                        severity=Severity.CRITICAL,
                        message='A fail state has a failure code of "123", the failure code should be a 4 digit code, found on line 8.'
                    ),
                ],
            ),
            (
                'tests/data/WARNING-StatesFailStateCodeReuseViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='StatesFailStateCodeReuseViolation',
                        severity=Severity.WARNING,
                        message='The code "1234" has been assigned 2 times in the states section, codes should not be reused.'
                    ),
                ],
            ),
        ],
    )
    def test_states_rules(self, process_file: str, prompts_file: str, expected_results: list[ValidationResult]) -> None:
        """
        Test states rule sets.

        :param process_file: The path to the process file.
        :param prompts_file: The path to the prompt file.
        :param expected_results: The expected validation results.
        """
        parser = Parser(process_file=process_file, prompts_file=prompts_file)
        process_content = parser.process_file
        prompts_content = parser.prompts_file

        config: dict[str, dict[str, bool | int | str]] = {}

        rule = States(prompts=prompts_content, process=process_content, config=config)
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)
        for result, expected in zip(results, expected_results):
            assert result.rule == expected.rule
            assert result.severity == expected.severity
            assert result.message == expected.message
