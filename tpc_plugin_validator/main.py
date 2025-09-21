"""Entry point for the TPC Plugin Validator module."""

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.utilities.types import CONFIG_TYPE
from tpc_plugin_validator.validator import Validator


def temp_entry(process_file: str, prompts_file: str) -> None:
    config: CONFIG_TYPE = {"logging": {"enabled": True}}
    parser = Parser(process_file=process_file, prompts_file=prompts_file)
    validator = Validator(parser=parser, config=config)
    validator.validate()
    result = validator.get_violations()
    print(result)


if __name__ == "__main__":
    print("This is a placeholder for the TPC Plugin Validator main module.")
    temp_entry(process_file="/tests/data/process.ini", prompts_file="/tests/data/prompts.ini")
