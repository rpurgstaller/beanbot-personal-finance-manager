from typing import Dict, List
from cli.validation import PathValidation
from examples import custom_style_3

from PyInquirer import prompt
from model.account import Account

from util.path import P_IMPORT


PATH_NAME = 'import_path'

CONFIRMATION_NAME = 'confirmation'

CLASS_OPTION = 'option'


def cust_prompt(arr : List):
    return prompt(arr, style=custom_style_3)
 

def cust_prompt_class_option(choices : Dict, message : str):
    action = cust_prompt(
        [
            get_option_list(choices.keys(), message)
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


def get_path(message : str, default=P_IMPORT):
    return {
        'type': 'input',
        'name': PATH_NAME,
        'message': message,
        'validate': PathValidation,
        'default': default
    }


def get_option_list(choices : List, message : str, name='option', when=None):
    return {
        'type': 'list',
        'message': message,
        'name': name,
        'choices': choices,
        'when': when
    }


def get_datatype_list(message : str = 'Choose datatype', name='datatype'):

    supported_datatypes = [
        {
            'name' : 'String',
            'value' : 'str'
        },
        {
            'name' : 'Float',
            'value' : 'float'
        },
        {
            'name' : 'Integer',
            'value' : 'int'
        }    
    ]

    return get_option_list(supported_datatypes, message, name)


def input(name, message, default=None, when=None):
    input_promt = {
        'type' : 'input',
        'name' : name,
        'message' : message
    }
    if default:
        input_promt['default'] = default

    if when:
        input_promt['when'] = when

    return input_promt

def account_chooser(name='account_id', message='Select account'):
    accounts = Account.get_all()
    if len(accounts) > 0:
        choices = [
            {
                'name': str(account),
                'value': account.id
            } for account in accounts
        ]
        return get_option_list(choices, message, name)

    print("No accounts existent")
    return None

def transaction_chooser(transactions, name='transaction_id', message='Select transaction'):
    if len(transactions) > 0:
        choices = [
            {
                'name': str(transaction),
                'value': transaction.id
            } for transaction in transactions
        ]
        return get_option_list(choices, message, name)

    print("No transactions existent")
    return None
