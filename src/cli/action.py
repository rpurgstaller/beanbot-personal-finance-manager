from abc import ABC, abstractmethod
from typing import List

from PyInquirer import prompt
from examples import custom_style_3

from beancount.core.account_types import DEFAULT_ACCOUNT_TYPES
from sqlalchemy.sql.expression import false
from cli.prompt import CLASS_OPTION, PATH_NAME, confirmation, cust_prompt, cust_prompt_class_option, get_class_option_list, get_path

from data_import.bank_importer import GiroImporter

from model.account import DbAccount


def returntomain(func):
    def wrap(*args, **kwargs):
        func(*args, **kwargs)
        ActionMain().prompt()
    return wrap


class Action(ABC):

    @abstractmethod
    def prompt(self) -> None:
        pass

    def execute(self) -> None:
        pass


class ActionMain(Action):

    def prompt(self):
        choices = {
            'Accounts': ActionAccountMain,
            'Transactions': ActionTransactionMain,
            'pizza': ActionPizza,
            'exit': ActionExit
        }

        cust_prompt_class_option(choices, 'choose option')


class ActionAccountMain(Action):

    def prompt(self) -> None:
        choices = {
            'Add account': ActionAddAccount,
            'List accounts': ActionListAccounts,
            'Delete Account': ActionDelAccount,
            'Import from CSV': ActionImportAccountCsv
        }

        cust_prompt_class_option(choices, 'choose option')


class ActionAddAccount(Action):

    @returntomain
    def prompt(self) -> None:
        self.action = cust_prompt([
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
        self.execute()

    def execute(self) -> None:
        DbAccount.build(**self.action)


class ActionListAccounts(Action):
    @returntomain
    def prompt(self) -> None:
        self.execute()

    def execute(self) -> None:
        accounts = DbAccount.get_all()
        print("Existing Accounts: ")
        for account in accounts:
            print(f'  - {str(account)}')


class ActionDelAccount(Action):
    @returntomain
    def prompt(self) -> None:
        accounts = DbAccount.get_all()
        self.action = cust_prompt([
            {
                'type': 'list',
                'name': 'account_id',
                'message': 'Select account to delete',
                'choices': [
                    {
                        'name': str(account),
                        'value': account.id
                    } for account in accounts
                ]
            },
            confirmation()
        ])
        self.execute()

    def execute(self) -> None:
        DbAccount.delete_by_id(self.action['account_id'])


class ActionImportAccountCsv(Action):
    @returntomain
    def prompt(self) -> None:
        self.action = cust_prompt([
            get_path('Please enter the path to the CSV file')
        ])
        self.execute()

    def execute(self) -> None:
        DbAccount.build_from_file(self.action[PATH_NAME])
        

class ActionTransactionMain(Action):

    def prompt(self) -> None:
        choices = {
            'Import from CSV': ActionTransactionImportCsv
        }

        cust_prompt_class_option(choices, 'choose option')


class ActionTransactionImportCsv(Action):

    @returntomain
    def prompt(self) -> None:
        self.action = cust_prompt([
            get_path('Please enter the path to the CSV file')
        ])
        self.execute()

    def execute(self) -> None:
        GiroImporter().execute(self.action[PATH_NAME])


class ActionPizza(Action):

    @returntomain
    def prompt(self) -> None:
        print('Pizza')

    def execute(self) -> None:
        return super().execute()


class ActionExit(Action):

    def prompt(self) -> None:
        self.execute()

    def execute(self) -> None:
        quit()


def run():
    ActionMain().prompt()