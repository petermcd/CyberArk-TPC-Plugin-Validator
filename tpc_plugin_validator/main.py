"""Entry point for the TPC Plugin Validator module."""

import argparse
import os
import sys

from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.validator import Validator


def main() -> None:
    """Main entry point for the TPC Plugin Validator module."""
    arg_parse = argparse.ArgumentParser(
        prog="CyberArk TPC Plugin Validator",
        description="Validate the provided TPC process and prompts file.",
    )
    arg_parse.add_argument("process_file", type=str, help="Path to the process file to validate")
    arg_parse.add_argument("prompts_file", type=str, help="Path to the prompts file to validate")
    args = arg_parse.parse_args()

    if not os.path.isfile(args.process_file):
        arg_parse.error(f'The process file "{args.process_file}" does not exist or is not accessible.')

    if not os.path.isfile(args.prompts_file):
        arg_parse.error(f'The prompts file "{args.prompts_file}" does not exist or is not accessible.')

    with open(args.process_file, "r", encoding="utf-8") as process_handler:
        process_file = process_handler.read()

    with open(args.prompts_file, "r", encoding="utf-8") as prompts_handler:
        prompts_file = prompts_handler.read()

    parser = Parser(process_file=process_file, prompts_file=prompts_file)
    validator = Validator(parser=parser, config={})
    validator.validate()
    result = validator.get_violations()
    print(result)

if __name__ == "__main__":
    sys.exit(main())