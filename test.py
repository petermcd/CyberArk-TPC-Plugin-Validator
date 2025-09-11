file_content='this wont match'
from tpc_plugin_validator.lexer.lexer import Lexer
lex = Lexer(source=file_content)
lex.process()
print(lex)