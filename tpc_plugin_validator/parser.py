"""Parser module for reading and processing configuration files."""
from configparser import ConfigParser

class Parser(object):
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
        self._process_file = ConfigParser()
        self._process_file.optionxform = str
        self._process_file.read(process_file)

        self._prompts_file = ConfigParser()
        self._prompts_file.optionxform = str
        self._prompts_file.read(prompts_file)

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

