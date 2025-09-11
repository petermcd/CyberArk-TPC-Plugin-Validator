"""Simple INI file parser."""
from os.path import isfile
from re import match

class IniParser(object):
    """A simple INI file parser."""
    def read(self, file_path: str) -> dict[str, list[str]]:
        """
        Read an INI file and return its contents as a dictionary.
        Each section is a key in the dictionary, and its value is a list of lines

        :param file_path: Path to the INI file.

        :return dict[str, list[str]]: A dictionary mapping section names to lists of lines.
        """
        parsed_data = {}
        current_section = 'default'
        current_lines = []

        if not isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r') as fh:
            while line := fh.readline():
                if str(line).strip().startswith('#'):
                    continue
                if not line.strip():
                    continue
                if self._is_section_header(text=line):
                    parsed_data[current_section] = current_lines
                    current_section = line.strip()[1:-1]
                    current_lines = []
                    continue
                current_lines.append(line.strip())
        parsed_data[current_section] = current_lines
        return parsed_data

    @staticmethod
    def _is_section_header(text: str) -> bool:
        section_regex = r'^\s*\[(.+)\]\s*$'
        return bool(match(section_regex, text))

