"""TypedDicts for various configurations used in the plugin validator."""

from typing import TypedDict

from tpc_plugin_validator.utilities.severity import Severity


class ValidSectionConfig(TypedDict):
    required: bool
    severity_level: Severity


CONFIG_TYPE = dict[str, dict[str, bool | int | str]]
