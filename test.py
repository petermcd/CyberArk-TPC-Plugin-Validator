from tpc_plugin_validator.utilities.types import SectionNames

section = "CPM Parameters Validation"

section_type = SectionNames.__getitem__(section)
print(type(section_type))
print(type(SectionNames.parameters))
