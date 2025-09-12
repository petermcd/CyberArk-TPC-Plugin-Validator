# Entry point for the TPC Plugin Validator module.
from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.logging import Logging


def temp_entry(process_file: str, prompts_file: str):
    parser = Parser(process_file=process_file, prompts_file=prompts_file)
    result = Logging(prompts=parser.prompts_file, process=parser.process_file, config={'enabled': True}).validate()
    print(result)

if __name__ == "__main__":
    print("This is a placeholder for the TPC Plugin Validator main module.")
    temp_entry(
        process_file='/tests/data/process.ini',
        prompts_file='/tests/data/prompts.ini'
    )
