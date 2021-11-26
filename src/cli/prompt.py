from typing import List
from cli.validations import PathValidation
from examples import custom_style_3

from PyInquirer import prompt

from util.path import IMPORT_PATH


PATH_NAME = 'import_path'

CONFIRMATION_NAME = 'confirmation'


def cust_prompt(arr : List):
    return prompt(arr, style=custom_style_3)


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