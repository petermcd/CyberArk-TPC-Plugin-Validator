"""Tests for the prompts rule set."""

import pytest

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.prompts import Prompts
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestPromptsRuleSets(object):
    """Tests for the prompts rule set."""

    @pytest.mark.parametrize(
        'process_file,prompts_file,expected_results',
        [
            (
                'tests/data/empty_process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='PromptsNoConditionSectionViolation',
                        severity=Severity.CRITICAL,
                        message='The prompts file does not contain a "conditions" section, therefore, the plugin cannot transitions between states.',
                    ),
                ],
            ),
            (
                'tests/data/WARNING-PromptsConditionTokenViolation/process.ini',
                'tests/data/WARNING-PromptsConditionTokenViolation/prompts.ini',
                [
                    ValidationResult(
                        rule='PromptsConditionTokenViolation',
                        severity=Severity.WARNING,
                        message='The token type "State Transition" is not valid in the "condition" section, found on line 3.',
                    ),
                ],
            ),
            (
                'tests/data/WARNING-PromptsInvalidSectionViolation/process.ini',
                'tests/data/WARNING-PromptsInvalidSectionViolation/prompts.ini',
                [
                    ValidationResult(
                        rule='PromptsInvalidSectionViolation',
                        severity=Severity.WARNING,
                        message='An invalid section "DummySection" has been found in the prompt file.',
                    ),
                ],
            ),
            (
                'tests/data/OK-PromptsDefaultContent-WithComment/process.ini',
                'tests/data/OK-PromptsDefaultContent-WithComment/prompts.ini',
                [],
            ),
            (
                'tests/data/OK-PromptsDefaultContent-WithoutComment/process.ini',
                'tests/data/OK-PromptsDefaultContent-WithoutComment/prompts.ini',
                [],
            ),
            (
                'tests/data/WARNING-PromptsDefaultContentViolation/process.ini',
                'tests/data/WARNING-PromptsDefaultContentViolation/prompts.ini',
                [
                    ValidationResult(
                        rule='PromptsDefaultContentViolation',
                        severity=Severity.WARNING,
                        message='A token of type "State Transition" has been found in the prompt file outwith a valid section on line 1.',
                    ),
                ],
            ),
            (
                'tests/data/WARNING-PromptsUnusedConditionViolation/process.ini',
                'tests/data/WARNING-PromptsUnusedConditionViolation/prompts.ini',
                [
                    ValidationResult(
                        rule='PromptsUnusedConditionViolation',
                        severity=Severity.WARNING,
                        message='The condition "hello" is declared in the prompts file on line 6 but is not used in the process file.',
                    ),
                ],
            ),
            (
                'tests/data/WARNING-PromptsDuplicateConditionViolation/process.ini',
                'tests/data/WARNING-PromptsDuplicateConditionViolation/prompts.ini',
                [
                    ValidationResult(
                        rule='PromptsDuplicateConditionViolation',
                        severity=Severity.WARNING,
                        message='The assignment "test" has been declared 2 times in the prompts file.',
                    ),
                ],
            ),
            (
                'tests/data/WARNING-PromptsConditionCaseMismatchViolation/process.ini',
                'tests/data/WARNING-PromptsConditionCaseMismatchViolation/prompts.ini',
                [
                    ValidationResult(
                        rule='PromptsConditionCaseMismatchViolation',
                        severity=Severity.WARNING,
                        message='A condition of "test" is declared but is used in the prompts file as "Test" on line 5.',
                    ),
                    ValidationResult(
                        rule='PromptsConditionCaseMismatchViolation',
                        severity=Severity.WARNING,
                        message='A condition of "test" is declared but is used in the prompts file as "tEst" on line 5.',
                    ),
                ],
            ),
        ],
    )
    def test_condition_used(self, process_file: str, prompts_file: str, expected_results: list[ValidationResult]):
        parser = Parser(process_file=process_file, prompts_file=prompts_file)
        process_content = parser.process_file
        prompts_content = parser.prompts_file

        rule = Prompts(prompts=prompts_content, process=process_content, config={})
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)
        for result, expected in zip(results, expected_results):
            assert result.rule == expected.rule
            assert result.severity == expected.severity
            assert result.message == expected.message