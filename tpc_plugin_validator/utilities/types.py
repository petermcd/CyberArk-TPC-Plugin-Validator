"""TypedDicts for various configurations used in the plugin validator."""

from enum import Enum
from typing import TypedDict

from tpc_plugin_validator.utilities.severity import Severity


CONFIG_TYPE = dict[str, dict[str, bool | int | str]]


class FileNames(Enum):
    """Enum to hold the valid file names."""

    process = "process.ini"
    prompts = "prompts.ini"


class SectionNames(Enum):
    """Enum to hold the valid section names."""

    cpm_parameters_validation = "CPM Parameters Validation"
    conditions = "conditions"
    debug_information = "Debug Information"
    default = "default"
    parameters = "parameters"
    states = "states"
    transitions = "transitions"


class ValidSectionConfig(TypedDict):
    required: bool
    severity_level: Severity


class Violations(Enum):
    """Enum to hold the valid violation types."""

    duplicate_assignment_violation = "DuplicateAssignmentViolation"
    duplicate_transition_violation = "DuplicateTransitionViolation"
    invalid_section_name_violation = "InvalidSectionNameViolation"
    invalid_token_type_violation = "InvalidTokenTypeViolation"
    invalid_transition_violation = "InvalidTransitionViolation"
    invalid_word_violation = "InvalidWordViolation"
    logging_enabled_violation = "LoggingEnabledViolation"
    missing_section_violation = "MissingSectionViolation"
    name_case_mismatch_violation = "NameCaseMismatchViolation"
    name_case_violation = "NameCaseViolation"
    name_violation = "NameViolation"
    parse_error_violation = "ParseErrorViolation"
    section_name_case_violation = "SectionNameCaseViolation"
    unused_condition_violation = "UnusedConditionViolation"
    unused_parameter_violation = "UnusedParameterViolation"
    value_case_violation = "ValueCaseViolation"
    value_violation = "ValueViolation"
