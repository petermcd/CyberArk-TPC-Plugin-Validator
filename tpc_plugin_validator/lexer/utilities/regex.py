"""List of regex the lexer uses."""


ASSIGNMENT = r'^(?:[\s]*)([\w]+)(?:(?:[\s]*)(=)((?:[\s]*)(((?!\s*fail\s*\().)+))?)?(?:[\s]*)$'
COMMENT = r'^(?:[\s]*)((?:[#;]+)(?:.*))(?:[\s]*)$'
CPM_PARAMETER_VALIDATION = r'^(?:[\s]*)(?P<name>[\w\\]+)(?:(?:[\s]*,[\s]*)(?:source)(?:[\s]*)=(?:[\s]*)(?P<source>[^, ]*))(?:(?:[\s]*,[\s]*)(?:mandatory)(?:[\s]*)=(?:[\s]*)(?P<mandatory>[^,]*))?(?:(?:[\s]*,[\s]*)(?:allowcharacters)(?:[\s]*)=(?:[\s]*)(?P<allowcharacters>.*))?$'
FAIL_STATE = r'^(?:[\s]*)([\w]+)(?:[\s]*)=(?:[\s]*)(?:[\s]*)(?:fail)(?:[\s]*)\((?:[\s]*)(.*)(?:[\s])?,(?:[\s]*)([0-9]+)\)(?:[\s]*)$'
SECTION_HEADER = r'^(?:[\s]*)\[([\w]+(?:[\s]+[\w]+)*)](?:[\s]*)$'
TRANSITION = r'^(?:[\s]*)([\w]+)(?:[\s]*,[\s]*)([\w]+)(?:[\s]*,[\s]*)([\w]+)(?:[\s]*)$'
