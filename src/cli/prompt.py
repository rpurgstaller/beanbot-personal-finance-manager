from cli.actions import ActionAddAccount
from cli.validations import PathValidation

from PyInquirer import prompt


DEFAULT_IMPORT_PATH = '/workspaces/beancount-cli/data'


def main_options():
    return prompt([
        {
            'type': 'rawlist',
            'message': 'Select option',
            'name': 'option',
            'choices': [
                'Add account', 'Import transactions', 'pizza'
            ]
        }
    ])

import_path = [
    {
        'type': 'input',
        'name': 'import_path',
        'message': f'Enter path',
        'validate': PathValidation,
        'default': DEFAULT_IMPORT_PATH
    }
]

