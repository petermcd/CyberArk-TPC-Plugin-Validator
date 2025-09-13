"""Tests for the process rule set."""

import pytest

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.process import Process
from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult


class TestProcessRuleSets(object):
    """Tests for the process rule set."""

    @pytest.mark.parametrize(
        'process_file,prompts_file,expected_results',
        [
            (
                'tests/data/WARNING-ProcessInvalidSectionViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='ProcessInvalidSectionViolation',
                        severity=Severity.WARNING,
                        message='An invalid section "DummySection" has been found in the process file.',
                    ),
                ],
            ),
            (
                'tests/data/OK-ProcessDefaultContent-WithComment/process.ini',
                'tests/data/empty_prompts.ini',
                [],
            ),
            (
                'tests/data/OK-ProcessDefaultContent-WithoutComment/process.ini',
                'tests/data/empty_prompts.ini',
                [],
            ),
            (
                'tests/data/WARNING-ProcessDefaultContentViolation/process.ini',
                'tests/data/empty_prompts.ini',
                [
                    ValidationResult(
                        rule='ProcessDefaultContentViolation',
                        severity=Severity.WARNING,
                        message='A token of type "State Transition" has been found in the process file outwith a valid section on line 5.',
                    ),
                ],
            ),
        ],
    )
    def test_process(self, process_file: str, prompts_file: str, expected_results: list[ValidationResult]):
        parser = Parser(process_file=process_file, prompts_file=prompts_file)
        process_content = parser.process_file
        prompts_content = parser.prompts_file

        rule = Process(prompts=prompts_content, process=process_content, config={})
        rule.validate()
        results = rule.get_violations()

        assert len(results) == len(expected_results)
        for result, expected in zip(results, expected_results):
            assert result.rule == expected.rule
            assert result.severity == expected.severity
            assert result.message == expected.message