from abc import ABC, abstractmethod
from typing import List

from PyInquirer import prompt
from examples import custom_style_3

from beancount.core.account_types import DEFAULT_ACCOUNT_TYPES
from sqlalchemy.sql.expression import false
from cli.prompt import CLASS_OPTION, PATH_NAME, account_chooser, confirmation, cust_prompt, cust_prompt_class_option, get_option_list, get_path, input

from data_import.bank_importer import GiroImporter

from model.account import Account
import os

from model.condition import ConditionIsExpense, ConditionIsIncome, ConditionRegexp
from model.rule import Rule

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
            'Rules' : ActionRuleMain,
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
        self.action = cust_prompt([
            account_chooser(message='Select account to delete'),
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


class ActionRuleMain(Action):

    def prompt(self) -> None:
        choices = {
            'Add Rule': ActionAddRule,
            'List Rules': ActionListRules,
            'Delete Rule': ActionDelRule
        }

        cust_prompt_class_option(choices, 'choose option')


class ActionAddRule(Action):

    @returntomain
    def prompt(self) -> None:
        self.action_rule = cust_prompt([
            account_chooser(message='Select account associated to the rule'),
            {
                'type': 'input',
                'message': 'Enter rule description',
                'name': 'name',
            }
        ])

        choices = {
            'Transformation': ActionCreateRuleTransformation,
            'Conditions': ActionCreateCondition,
            'Done' : None
        }

        #self.transformations = []
        #self.conditions = []

        #action_results = {
        #    ActionCreateRuleTransformation : lambda action_result : self.transformations.append(action_result),
        #    ActionCreateCondition : lambda action_result : self.conditions.append(action_result)
        #}

        self.action_results = []

        while 1:
            action_class = cust_prompt(get_option_list(choices.keys(), "Chose option"))['option']
            if not action_class:
                break

            action_instance = action_class()
            action_instance.prompt()
            self.action_results.append(action_instance)

        self.execute()

    def execute(self) -> None:
        rule_params = self.action_rule
        action_results = self.action_results


class ActionCreateRuleTransformation(Action):

    TRANSACTION_ATTRIBUTES = {
        'partner_account_id' : 'partner account',
        'partner_name' : 'partner name'
    }

    @returntomain
    def prompt(self) -> None:
        self.action = cust_prompt([
            {
                get_option_list(ActionCreateRuleTransformation.TRANSACTION_ATTRIBUTES, "Choose transaction attribute to transform", 
                    name='transaction_attribute'),
    
            }
        ])

    def execute(self) -> None:
        pass


class ActionListRules(Action):

    @returntomain
    def prompt(self) -> None:
        self.execute()

    def execute(self) -> None:
        rules = Rule.get_all()
        print("Existing Rules: ")
        for rule in rules:
            print(f'  - {str(rule)}')


class ActionDelRule(Action):
    @returntomain
    def prompt(self) -> None:
        rules = Rule.get_all()
        self.action = cust_prompt([
            {
                'type': 'list',
                'name': 'rule_id',
                'message': 'Select rule to delete',
                'choices': [
                    {
                        'name': str(rule),
                        'value': rule.id
                    } for rule in rules
                ]
            },
            confirmation()
        ])
        self.execute()

    def execute(self) -> None:
        Rule.delete_by_id(self.action['rule_id'])


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
            get_option_list(ActionCreateCondition.CONDITION_TYPES.keys(), 'Choose condition type'),
            input('regexp', 'Enter regexp', when=regexp_prompt_lambda),
            get_option_list(ActionCreateCondition.TRANSACTION_ATTRIBUTES, 'Choose transaction attribute', 
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