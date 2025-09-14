"""Tests for the transition rule set."""

import pytest

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.transitions import Transitions
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestProcessRuleSets(object):
    """Tests for the process rule set."""

    @pytest.mark.parametrize(
        'process_file,prompts_file,expected_results',
        [
            (
                'tests/data/CRITICAL-TransitionNoSectionViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='TransitionNoSectionViolation',
                        severity=Severity.CRITICAL,
                        message='The process file does not contain a "transitions" section.',
                    ),
                ],
            ),
            (
                'tests/data/WARNING-SectionCaseMismatchViolation-Transitions/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='SectionCaseMismatchViolation',
                        severity=Severity.WARNING,
                        message='The "transitions" section has been declared as "Transitions".',
                    ),
                ],
            ),
            (
                'tests/data/WARNING-TransitionsStateTransitionReuseViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='TransitionsStateTransitionReuseViolation',
                        severity=Severity.WARNING,
                        message='The state transition "state1,condition,state2" has been declared 2 times, a state transition should be unique.',
                    ),
                ],
            ),
            (
                'tests/data/WARNING-TransitionsTokenViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='TransitionsTokenViolation',
                        severity=Severity.WARNING,
                        message='The token type "Assignment" is not valid in the "transitions" section, found on line 9.',
                    ),
                ],
            ),
            (
                'tests/data/WARNING-TransitionsStateTransitionViolation-InvalidNext/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='TransitionsStateTransitionViolation',
                        severity=Severity.WARNING,
                        message='The state "state3" does not have a valid state to transition too.',
                    ),
                ],
            ),
            (
                'tests/data/WARNING-TransitionsStateTransitionViolation-InvalidPrevious/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='TransitionsStateTransitionViolation',
                        severity=Severity.WARNING,
                        message='The state "state3" does not have a valid state to transition from.',
                    ),
                ],
            ),
        ],
    )
    def test_state_transitions(self, process_file: str, prompts_file: str, expected_results: list[ValidationResult]):
        parser = Parser(process_file=process_file, prompts_file=prompts_file)
        process_content = parser.process_file
        prompts_content = parser.prompts_file

        rule = Transitions(prompts=prompts_content, process=process_content, config={})
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)
        for result, expected in zip(results, expected_results):
            assert result.rule == expected.rule
            assert result.severity == expected.severity
            assert result.message == expected.message