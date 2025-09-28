# CyberArk TPC Plugin Validator

CyberArk TPC Plugin Validator is a tool designed to validate third party CyberArk TPC plugins.
It ensures that the plugins meet the required standards helping to ensure that they will work within the CyberArk
ecosystem.

## Installation

To install the CyberArk TPC Plugin Validator, you can use pip:

```bash
pip install cyberark-tpc-plugin-validator
```

## Usage

The tool can be run from the command line. It takes the path to the process and prompts files as an argument.

```bash
tpc-validator \path\to\plugin\directory\process.ini \path\to\plugin\directory\prompts.ini
```

Alternatively you can run it using Python directly:

```python
from tpc_plugin_validator.validator import Validator
validator = Validator.with_file(r'\path\to\plugin\directory\process.ini', r'\path\to\plugin\directory\prompts.ini', {})
validator.validate()
print(validator.get_violations())
```

