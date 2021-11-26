from abc import ABC, abstractmethod
from typing import List

from PyInquirer import prompt
from examples import custom_style_3

from beancount.core.account_types import DEFAULT_ACCOUNT_TYPES
from sqlalchemy.sql.expression import false
from cli.prompt import PATH_NAME, confirmation, cust_prompt, get_path
from cli.validations import PathValidation

from data_import.csv_importer import CsvImporter

from model.account import DbAccount


def returntomain(func):
    def wrap(*args, **kwargs):
        func(*args, **kwargs)
        ActionMain().execute()
    return wrap


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
            'CSV Import': ActionImportCSV,
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


class ActionImportCSV(Action):
    def execute(self) -> str:
        choices = {
            'Import Transactions': ActionImportTransactions,
            'Import accounts': ActionImportCSVAccounts,
            'Cancel': ActionMain
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


class ActionImportCSVAccounts(Action):
    @returntomain
    def execute(self) -> None:
        action = cust_prompt([
            get_path('Please enter the path to the CSV file')
        ])

        CsvImporter().execute(action[PATH_NAME], DbAccount)
        




