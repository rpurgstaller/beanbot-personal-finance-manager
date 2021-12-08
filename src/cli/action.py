from abc import ABC, abstractmethod
from typing import List

from PyInquirer import prompt
from examples import custom_style_3

from beancount.core.account_types import DEFAULT_ACCOUNT_TYPES
from sqlalchemy.sql.expression import false
from cli.prompt import CLASS_OPTION, PATH_NAME, confirmation, cust_prompt, cust_prompt_class_option, get_class_option_list, get_path, input

from data_import.bank_importer import GiroImporter

from model.account import Account
import os

from model.condition import ConditionIsExpense, ConditionIsIncome, ConditionRegexp

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
        Account.build(**self.action)


class ActionListAccounts(Action):
    @returntomain
    def prompt(self) -> None:
        self.execute()

    def execute(self) -> None:
        accounts = Account.get_all()
        print("Existing Accounts: ")
        for account in accounts:
            print(f'  - {str(account)}')


class ActionDelAccount(Action):
    @returntomain
    def prompt(self) -> None:
        accounts = Account.get_all()
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
        Account.delete_by_id(self.action['account_id'])


class ActionImportAccountCsv(Action):
    @returntomain
    def prompt(self) -> None:
        self.action = cust_prompt([
            get_path('Please enter the path to the CSV file')
        ])
        self.execute()

    def execute(self) -> None:
        Account.build_from_file(self.action[PATH_NAME])
        

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
            get_path('Enter the path to the CSV file')
        ])

        self.path_name = self.action[PATH_NAME]

        self.execute()

    def execute(self) -> None:
        GiroImporter(os.environ['BEANBOT_GIRO_ACCOUNT']).execute(self.path_name)


class ActionCreateRule(Action):

    @returntomain
    def prompt(self) -> None:
        self.action = cust_prompt([
            {

            }
        ])

    def execute(self) -> None:
        pass


class ActionCreateRuleTransformation(Action):

    TRANSACTION_ATTRIBUTES = {
        'partner_account_id' : 'partner account',
        'partner_name' : 'partner name'
    }

    @returntomain
    def prompt(self) -> None:
        self.action = cust_prompt([
            {

            }
        ])

    def execute(self) -> None:
        pass


class ActionCreateCondition(Action):

    CONDITION_TYPES = {
        'Regexp' : ConditionRegexp,
        'Is Income' : ConditionIsIncome,
        'Is Expense' : ConditionIsExpense
    }

    TRANSACTION_ATTRIBUTES = {
        'reference' : 'reference',
        'partner_name' : 'partner name'
    }
        
    @returntomain
    def prompt(self) -> None:

        regexp_prompt_lambda = lambda answers: answers['option'] == 'Regexp'

        self.action = cust_prompt([
            get_class_option_list(ActionCreateCondition.CONDITION_TYPES.keys(), 'Choose condition type'),
            input('regexp', 'Enter regexp', when=regexp_prompt_lambda),
            get_class_option_list(ActionCreateCondition.TRANSACTION_ATTRIBUTES, 'Choose transaction attribute', 
                when=regexp_prompt_lambda)
        ])

    def execute(self) -> None:
        x = self.action


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