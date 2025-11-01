from tpc_plugin_validator.rule_sets.states_section_rule_set import StatesSectionRuleSet
from tpc_plugin_validator.validator import Validator

process_file='tests/data/invalid-process.ini',
prompts_file='tests/data/valid-prompts.ini',


validator = Validator.with_file(
    process_file_path=process_file,
    prompts_file_path=prompts_file,
    config={},
)

validator.validate()
violations = validator.get_violations()
print(violations)

