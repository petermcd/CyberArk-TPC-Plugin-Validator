"""Entry point for the TPC Plugin Validator module."""

import argparse
import sys

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

    try:
        validator = Validator.with_file(
            process_file_path=args.process_file, prompts_file_path=args.prompts_file, config={}
        )
    except FileNotFoundError:
        print("One or both of the specified files do not exist.")
        sys.exit(1)

    validator.validate()
    violations = validator.get_violations()

    if not violations:
        print("No violations found. The files are valid.")
        sys.exit(0)

    print(f"{len(violations)} violations found:")
    for violation in violations:
        print(f"{violation.severity} - {violation.rule} - {violation.message}")

    sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
