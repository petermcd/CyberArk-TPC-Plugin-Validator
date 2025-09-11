"""Parser module for reading and processing configuration files."""
from tpc_plugin_validator.lexer.lexer import Lexer
from tpc_plugin_validator.lexer.utilities.token_name import TokenName


class Parser(object):
    """Object to handle parsing ini files."""
    __slots__ = (
        '_process_file',
        '_prompts_file',
    )

    def __init__(self, process_file: str, prompts_file: str) -> None:
        """
        Initializes the Parser with the given process and prompts files.

        :param process_file (str): Path to the process configuration file.
        :param prompts_file (str): Path to the prompt configuration file.
        """

        with open(process_file, 'r', encoding='utf-8') as process_handler:
            process_lexer = Lexer(source=process_handler.read())
            self._prepare_process(lexed_process=process_lexer)

        with open(prompts_file, 'r', encoding='utf-8') as prompts_handler:
            prompts_lexer = Lexer(source=prompts_handler.read())
            self._prepare_prompts(lexed_prompts=prompts_lexer)

    def _prepare_prompts(self, lexed_prompts: Lexer):
        """
        Prepare the prompts file from the lexed result.

        :param lexed_prompts: Result of lexing the prompts file.
        """
        self._prompts_file = self._process_lex(lexed_file=lexed_prompts)

    def _prepare_process(self, lexed_process: Lexer):
        """
        Prepare the process file from the lexed result.

        :param lexed_process: Result of lexing the process file.
        """
        self._process_file = self._process_lex(lexed_file=lexed_process)

    @staticmethod
    def _process_lex(lexed_file: Lexer):
        """
        Process a lex and return the results.

        :param lexed_file: Result of lexing a file.

        :return: Result of processing the lexed file.
        """
        current_section_name: str = 'default'
        section_entries = []
        sorted_lex = {}
        for lexed_line in lexed_file.tokens:
            if lexed_line[0] == TokenName.SECTION_HEADER:
                sorted_lex[current_section_name] = section_entries
                current_section_name = lexed_line[1].name
                section_entries = []
                continue
            section_entries.append(lexed_line[1])
        sorted_lex[current_section_name] = section_entries
        return sorted_lex

    @property
    def process_file(self):
        """
        Returns the parsed process configuration.

        :return: ConfigParser object containing the process file.
        """
        return self._process_file

    @property
    def prompts_file(self):
        """
        Returns the parsed prompts file.

        :return: ConfigParser object containing the prompt file.
        """
        return self._prompts_file
