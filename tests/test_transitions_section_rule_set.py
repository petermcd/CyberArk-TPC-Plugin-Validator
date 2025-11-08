"""Tests for the transitions section rule set."""

import pytest

from tpc_plugin_validator.utilities.severity import Severity
from tpc_plugin_validator.utilities.validation_result import ValidationResult
from tpc_plugin_validator.validator import Validator


class TestTransitionsSectionRuleSet(object):
    """Tests for the transitions section rule set."""

    @pytest.mark.parametrize(
        "process_file,prompts_file,expected_violations",
        [
            (
                "tests/data/transitions-invalid-process.ini",
                "tests/data/transitions-invalid-prompts.ini",
                [
                    # Test to ensure duplicate transitions are caught.
                    ValidationResult(
                        rule="DuplicateTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The transition "wait,failure,somefailure" has been declared 2 times, a transition triple must be unique.',
                        file="process.ini",
                        section="transitions",
                    ),
                    # Test to ensure that the init name is caught if anything other than Init.
                    ValidationResult(
                        rule="NameViolation",
                        severity=Severity.WARNING,
                        message='The start state "Begin", for clarity should be called "Init".',
                        file="process.ini",
                        section="transitions",
                        line=21,
                    ),
                    # Test to ensure states in transitions are in the same case as they are declared.
                    ValidationResult(
                        rule="NameCaseMismatchViolation",
                        severity=Severity.WARNING,
                        message='The state "Wait" is declared but is used with different casing in the transition next state.',
                        file="process.ini",
                        section="transitions",
                        line=21,
                    ),
                    # Test to ensure states in transitions are in the same case as they are declared.
                    ValidationResult(
                        rule="NameCaseMismatchViolation",
                        severity=Severity.WARNING,
                        message='The state "Wait" is declared but is used with different casing in the transition current state.',
                        file="process.ini",
                        section="transitions",
                        line=22,
                    ),
                    # Test to ensure that conditions used in transitions have been declard.
                    ValidationResult(
                        rule="InvalidConditionViolation",
                        severity=Severity.CRITICAL,
                        message='The condition "SQL" used in the transition from "IsWaiting" to "END" but has not been declared.',
                        file="process.ini",
                        section="transitions",
                        line=24,
                    ),
                    # Test to ensure that transitions that cannot be reached are caught.
                    ValidationResult(
                        rule="UnreachableTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The transition "IsWaiting,Waiting,END" is unreachable due to a previous transition from "IsWaiting" having a boolean condition.',
                        file="process.ini",
                        section="transitions",
                        line=26,
                    ),
                    # Test to ensure states in transitions are in the same case as they are declared.
                    ValidationResult(
                        rule="NameCaseMismatchViolation",
                        severity=Severity.WARNING,
                        message='The condition "Failure" is declared but is used as "failure".',
                        file="process.ini",
                        section="transitions",
                        line=28,
                    ),
                    # Test to ensure that transitions can be reached.
                    ValidationResult(
                        rule="InvalidTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The state "NoPrevious" does not have a valid transition leading to it.',
                        file="process.ini",
                        section="transitions",
                        line=29,
                    ),
                    # Test to ensure that states used in transitions have been declared.
                    ValidationResult(
                        rule="InvalidTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The state "NoPrevious" used in the transition current state has not been declared.',
                        file="process.ini",
                        section="transitions",
                        line=29,
                    ),
                    # Test to ensure that states in transitions have been declared.
                    ValidationResult(
                        rule="InvalidTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The state "NoNext" used in the transition next state has not been declared.',
                        file="process.ini",
                        section="transitions",
                        line=31,
                    ),
                    # Test to ensure that states in transitions have been declared.
                    ValidationResult(
                        rule="InvalidTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The state "Wait" attempts to transition to "NoNext" but has not been declared.',
                        file="process.ini",
                        section="transitions",
                        line=31,
                    ),
                    # Test to ensure that transitions that cannot be reached are caught.
                    ValidationResult(
                        rule="UnreachableTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The transition "Wait,Nothing,NoNext" is unreachable due to a previous transition from "Wait" having a boolean condition.',
                        file="process.ini",
                        section="transitions",
                        line=31,
                    ),
                    # Test invalid token type in transitions section are caught.
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.CRITICAL,
                        message='The token type "Assignment" is not valid in the "transitions" section.',
                        file="process.ini",
                        section="transitions",
                        line=33,
                    ),
                    # Test for ensuring parse errors are caught.
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed correctly.",
                        file="process.ini",
                        section="transitions",
                        line=34,
                    ),
                ],
            ),
            (
                # Test to ensure that validation continues with a missing prompts file.
                "tests/data/transitions-invalid-process.ini",
                None,
                [
                    ValidationResult(
                        rule="InformationOnly",
                        severity=Severity.INFO,
                        message="The prompts file was not supplied, therefore, assumptions have been made of boolean conditions. Transitions that rely on boolean conditions may not validate correctly.",
                        file="process.ini",
                    ),
                    ValidationResult(
                        rule="UnusedParameterViolation",
                        severity=Severity.WARNING,
                        message='The parameter "username" has been validated but is not used.',
                        file="process.ini",
                        section="CPM Parameters Validation",
                        line=39,
                    ),
                    # Test to ensure duplicate transitions are caught.
                    ValidationResult(
                        rule="DuplicateTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The transition "wait,failure,somefailure" has been declared 2 times, a transition triple must be unique.',
                        file="process.ini",
                        section="transitions",
                    ),
                    # Test to ensure that the init name is caught if anything other than Init.
                    ValidationResult(
                        rule="NameViolation",
                        severity=Severity.WARNING,
                        message='The start state "Begin", for clarity should be called "Init".',
                        file="process.ini",
                        section="transitions",
                        line=21,
                    ),
                    # Test to ensure states in transitions are in the same case as they are declared.
                    ValidationResult(
                        rule="NameCaseMismatchViolation",
                        severity=Severity.WARNING,
                        message='The state "Wait" is declared but is used with different casing in the transition next state.',
                        file="process.ini",
                        section="transitions",
                        line=21,
                    ),
                    # Test to ensure states in transitions are in the same case as they are declared.
                    ValidationResult(
                        rule="NameCaseMismatchViolation",
                        severity=Severity.WARNING,
                        message='The state "Wait" is declared but is used with different casing in the transition current state.',
                        file="process.ini",
                        section="transitions",
                        line=22,
                    ),
                    # Test to ensure that transitions that cannot be reached are caught.
                    ValidationResult(
                        rule="UnreachableTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The transition "IsWaiting,Waiting,END" is unreachable due to a previous transition from "IsWaiting" having a boolean condition.',
                        file="process.ini",
                        section="transitions",
                        line=26,
                    ),
                    # Test to ensure that transitions can be reached.
                    ValidationResult(
                        rule="InvalidTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The state "NoPrevious" does not have a valid transition leading to it.',
                        file="process.ini",
                        section="transitions",
                        line=29,
                    ),
                    # Test to ensure that states used in transitions have been declared.
                    ValidationResult(
                        rule="InvalidTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The state "NoPrevious" used in the transition current state has not been declared.',
                        file="process.ini",
                        section="transitions",
                        line=29,
                    ),
                    # Test to ensure that states in transitions have been declared.
                    ValidationResult(
                        rule="InvalidTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The state "NoNext" used in the transition next state has not been declared.',
                        file="process.ini",
                        section="transitions",
                        line=31,
                    ),
                    # Test to ensure that states in transitions have been declared.
                    ValidationResult(
                        rule="InvalidTransitionViolation",
                        severity=Severity.CRITICAL,
                        message='The state "Wait" attempts to transition to "NoNext" but has not been declared.',
                        file="process.ini",
                        section="transitions",
                        line=31,
                    ),
                    # Test invalid token type in transitions section are caught.
                    ValidationResult(
                        rule="InvalidTokenTypeViolation",
                        severity=Severity.CRITICAL,
                        message='The token type "Assignment" is not valid in the "transitions" section.',
                        file="process.ini",
                        section="transitions",
                        line=33,
                    ),
                    # Test for ensuring parse errors are caught.
                    ValidationResult(
                        rule="ParseErrorViolation",
                        severity=Severity.CRITICAL,
                        message="Line could not be parsed correctly.",
                        file="process.ini",
                        section="transitions",
                        line=34,
                    ),
                ],
            ),
            (
                # Test to ensure that validation continues with a missing prompts file.
                "tests/data/valid-process.ini",
                None,
                [
                    ValidationResult(
                        rule="InformationOnly",
                        severity=Severity.INFO,
                        message="The prompts file was not supplied, therefore, assumptions have been made of boolean conditions. Transitions that rely on boolean conditions may not validate correctly.",
                        file="process.ini",
                    ),
                    ValidationResult(  # Valid as the username is used in the prompts file which is missing in this test.
                        rule="UnusedParameterViolation",
                        severity=Severity.WARNING,
                        message='The parameter "username" has been validated but is not used.',
                        file="process.ini",
                        section="CPM Parameters Validation",
                        line=30,
                    ),
                ],
            ),
            (
                # Test to ensure that validation continues with a missing process file.
                None,
                "tests/data/valid-prompts.ini",
                [],
            ),
        ],
    )
    def test_transitions_section_rule_set(
        self,
        process_file: str,
        prompts_file: str,
        expected_violations: list[ValidationResult],
    ) -> None:
        """
        Tests for the transitions section rule set.

        :param process_file: Path to the process file to use for the test case.
        :param prompts_file: Path to the prompts file to use for the test case.
        :param expected_violations: List of expected ValidationResult
        """
        validate = Validator.with_file(prompts_file_path=prompts_file, process_file_path=process_file)
        validate.validate()
        results = validate.get_violations()

        assert len(results) == len(expected_violations)

        for result in results:
            assert result in expected_violations

        assert validate.get_violations() == expected_violations
