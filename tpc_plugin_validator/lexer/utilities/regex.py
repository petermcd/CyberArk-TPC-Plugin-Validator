"""List of regex the lexer uses."""


ASSIGNMENT = r'^(?:[\s]*)([\w]+)(?:(?:[\s]*)(=)((?:[\s]*)(.+))?)?(?:[\s]*)$'
COMMENT = r'^(?:[\s]*)((?:[#;]+)(?:.*))(?:[\s]*)$'
FAIL_STATE = r'^(?:[\s]*)(?:fail|FAIL)(?:[\s]*)\((?:[\s]*)(?:\'|\")(.*)(?:\'|\")(?:[\s,]*)([0-9]*)\)(?:[\s]*)$'
CPM_PARAMETER_VALIDATION = r'^(?:[\s]*)(?P<name>[\w\\]+)(?:(?:[\s]*,[\s]*)(?:source)(?:[\s]*)=(?:[\s]*)(?P<source>[^, ]*))(?:(?:[\s]*,[\s]*)(?:mandatory)(?:[\s]*)=(?:[\s]*)(?P<mandatory>[^,]*))?(?:(?:[\s]*,[\s]*)(?:allowcharacters)(?:[\s]*)=(?:[\s]*)(?P<allowcharacters>.*))?$'
SECTION_HEADER = r'^(?:[\s]*)\[([\w]+(?:[\s]+[\w]+)*)](?:[\s]*)$'
TRANSITION = r'^(?:[\s]*)([\w]+)(?:[\s]*,[\s]*)([\w]+)(?:[\s]*,[\s]*)([\w]+)(?:[\s]*)$'
