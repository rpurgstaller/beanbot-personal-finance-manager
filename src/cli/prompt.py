from typing import Dict, List
from cli.validation import PathValidation
from examples import custom_style_3

from PyInquirer import prompt

from util.path import IMPORT_PATH


PATH_NAME = 'import_path'

CONFIRMATION_NAME = 'confirmation'

CLASS_OPTION = 'option'


def cust_prompt(arr : List):
    return prompt(arr, style=custom_style_3)
 

def cust_prompt_class_option(choices : Dict, message : str):
    action = cust_prompt(
        [
            get_class_option_list(choices.keys(), message)
        ]
    )

    action = choices[action[CLASS_OPTION]]()
    action.prompt()


def confirmation(message : str = 'Are you sure?'):
    return {
                'type': 'confirm',
                'name': CONFIRMATION_NAME,
                'message': message,
                'default': True
            }


def get_path(message : str):
    return {
                'type': 'input',
                'name': PATH_NAME,
                'message': message,
                'validate': PathValidation,
                'default': IMPORT_PATH
            }


def get_class_option_list(choices : List, message : str):
    return {
                'type': 'list',
                'message': message,
                'name': 'option',
                'choices': choices
            }