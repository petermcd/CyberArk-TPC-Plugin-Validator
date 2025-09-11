"""List of regex the lexer uses."""

# Reused regexes
STANDARD_WORD = r'[\w]+'
STATE_NAME = STANDARD_WORD
VARIABLE_NAME = STANDARD_WORD
VARIABLE_VALUE = STANDARD_WORD

# Punctuation
SPACE_COMMA = r'[\s,]'
SPACES = r'[\s]*'

COMMENT = fr'^(?:{SPACES})((?:[#;]+)(?:.*))(?:{SPACES})$'
SECTION_HEADER_NAME = r'([\w]+[\w\s]+[\w]+)'
SECTION_HEADER = fr'^(?:{SPACES})\[{SECTION_HEADER_NAME}](?:{SPACES})$'
CONDITION_NAME = r'[\w]+'
TRANSITION = fr'^(?:{SPACES})({STATE_NAME})(?:{SPACE_COMMA}+)({CONDITION_NAME})(?:{SPACE_COMMA}+)({STATE_NAME})(?:{SPACES})$'
ASSIGNMENT = fr'^(?:{SPACES})({VARIABLE_NAME})(?:(?:{SPACES})(=)((?:{SPACES})({VARIABLE_VALUE}))?)?(?:{SPACES})$'
FAIL_CODE = r'[0-9]{4}'
FAIL_MESSAGE = r'.*'
FAIL_STATE = fr'^(?:{SPACES})(?:fail|FAIL)(?:{SPACES})\((?:{SPACES})(?:\'|\")({FAIL_MESSAGE})(?:\'|\")(?:{SPACE_COMMA}*)({FAIL_CODE})\)(?:{SPACES})$'
