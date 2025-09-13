from tpc_plugin_validator.parser.parser import Parser
from tpc_plugin_validator.rule_sets.parameters import Parameters

process_file = 'tests/data/CRITICAL-ParameterMinGreaterThanMaxViolation/process.ini'
prompts_file = 'tests/data/empty_prompts.ini'
parser = Parser(process_file=process_file, prompts_file=prompts_file)
process_content = parser.process_file
prompts_content = parser.prompts_file

rule = Parameters(prompts=prompts_content, process=process_content, config={})
rule.validate()
print(rule)