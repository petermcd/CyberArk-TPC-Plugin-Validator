"""Parser module for reading and processing configuration files."""
import os

from tpc_plugin_validator.lexer.lexer import Lexer
from tpc_plugin_validator.lexer.tokens.assignment import Assignment
from tpc_plugin_validator.lexer.tokens.comment import Comment
from tpc_plugin_validator.lexer.tokens.cpm_parameter_validation import \
    CPMParameterValidation
from tpc_plugin_validator.lexer.tokens.fail_state import FailState
from tpc_plugin_validator.lexer.tokens.section_header import SectionHeader
from tpc_plugin_validator.lexer.tokens.transition import Transition
from tpc_plugin_validator.lexer.utilities.token_name import TokenName


class Parser(object):
    """Object to handle parsing ini files."""
    __slots__ = (
        '_process_file',
        '_process_file_path',
        '_prompts_file',
        '_prompts_file_path',
    )

    def __init__(self, process_file: str, prompts_file: str) -> None:
        """
        Initializes the Parser with the given process and prompts files.

        :param process_file (str): Path to the process configuration file.
        :param prompts_file (str): Path to the prompt configuration file.
        """
        self._process_file_path = process_file
        self._prompts_file_path = prompts_file

        if not os.path.isfile(self._process_file_path):
            raise FileNotFoundError(f'The process file "{self._process_file_path}" does not exist or is not accessible.')

        if not os.path.isfile(self._prompts_file_path):
            raise FileNotFoundError(f'The prompts file "{self._prompts_file_path}" does not exist or is not accessible.')

        with open(self._process_file_path, 'r', encoding='utf-8') as process_handler:
            process_lexer = Lexer(source=process_handler.read())
            self._prepare_process(lexed_process=process_lexer)

        with open(self._prompts_file_path, 'r', encoding='utf-8') as prompts_handler:
            prompts_lexer = Lexer(source=prompts_handler.read())
            self._prepare_prompts(lexed_prompts=prompts_lexer)

    def _prepare_process(self, lexed_process: Lexer) -> None:
        """
        Prepare the process file from the lexed result.

        :param lexed_process: Result of lexing the process file.
        """
        self._process_file = self._process_lex(lexed_file=lexed_process)

    def _prepare_prompts(self, lexed_prompts: Lexer) -> None:
        """
        Prepare the prompts file from the lexed result.

        :param lexed_prompts: Result of lexing the prompts file.
        """
        self._prompts_file = self._process_lex(lexed_file=lexed_prompts)

    @staticmethod
    def _process_lex(lexed_file: Lexer):
        """
        Process a lex and return the results.

        :param lexed_file: Result of lexing a file.

        :return: Result of processing the lexed file.
        """
        current_section_name: str = 'default'
        section_entries: list[Assignment | Comment | FailState | CPMParameterValidation | SectionHeader | Transition] = []
        sorted_lex = {}
        for lexed_line in lexed_file.tokens:
            if lexed_line[0] == TokenName.SECTION_HEADER:
                sorted_lex[current_section_name] = section_entries
                if type(lexed_line[1]) is SectionHeader:
                    current_section_name = lexed_line[1].name
                else:
                    # This should never be reached, this is here to satisfy typing.
                    current_section_name = 'UNKNOWN'
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
