from abc import ABC, abstractmethod
from typing import List

from PyInquirer import prompt
from examples import custom_style_3

from beancount.core.account_types import DEFAULT_ACCOUNT_TYPES
from sqlalchemy.sql.expression import false

from model.account import DbAccount


def returntomain(func):
    def wrap(*args, **kwargs):
        func(*args, **kwargs)
        ActionMain().execute()
    return wrap


def confirmation():
    return {
                'type': 'confirm',
                'message': 'Are you sure?',
                'name': 'confirmation',
                'default': True
            }


def cust_prompt(arr : List):

    return prompt(arr, style=custom_style_3)


class Action(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass


class ActionMain(Action):

    def execute(self) -> str:
        choices = {
            'Add account': ActionAddAccount,
            'List accounts': ActionListAccounts,
            'Delete Account': ActionDelAccount,
            'Import transactions': ActionImportTransactions,
            'pizza': ActionPizza,
            'exit': ActionExit
        }

        action = cust_prompt([
            {
                'type': 'list',
                'message': 'Select option',
                'name': 'option',
                'choices': choices.keys()
            }
        ])

        action = choices[action['option']]()
        action.execute()


class ActionAddAccount(Action):

    @returntomain
    def execute(self) -> None:
        action = cust_prompt([
            {
                'type': 'list',
                'message': 'Select account type',
                'name': 'account_type',
                'choices': DEFAULT_ACCOUNT_TYPES
            },
            {
                'type': 'input',
                'message': 'Enter account name',
                'name': 'name',
            },
            {
                'type': 'input',
                'message': 'Enter account key',
                'name': 'key',
            }
        ])
        DbAccount.build(action)


class ActionListAccounts(Action):
    @returntomain
    def execute(self) -> None:
        accounts = DbAccount.get_all()
        print("Existing Accounts: ")
        for account in accounts:
            print(f'  - {str(account)}')


class ActionDelAccount(Action):
    @returntomain
    def execute(self) -> None:
        accounts = DbAccount.get_all()
        action = cust_prompt([
            {
                'type': 'list',
                'name': 'account_id',
                'message': 'Select account to delete',
                'choices': [
                    {
                        'name': str(account),
                        'value': account.key
                    } for account in accounts
                ]
            },
            confirmation()
        ])

        x = action


class ActionImportTransactions(Action):

    @returntomain
    def execute(self) -> None:
        print('Execute: Import Transactions')


class ActionPizza(Action):

    @returntomain
    def execute(self) -> None:
        print('pizza')


class ActionExit(Action):

    def execute(self) -> None:
        quit()