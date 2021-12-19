from abc import ABC, abstractmethod
from typing import List

from PyInquirer import prompt
from examples import custom_style_3

from beancount.core.account_types import DEFAULT_ACCOUNT_TYPES
from sqlalchemy.sql.expression import false
from cli.prompt import CLASS_OPTION, CONFIRMATION_NAME, PATH_NAME, account_chooser, confirmation, cust_prompt, cust_prompt_class_option, get_datatype_list, get_option_list, get_path, input

from data_import.bank_importer import TransactionImporter

from model.account import Account

from model.condition import ConditionIsExpense, ConditionIsIncome, ConditionRegexp
from model.rule import Rule
from model.rule_transformation import RuleTransformation
from util.path import P_BEANCOUNT
from beancount_import.writer import write_all as beancount_write_all

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
            'Beancount' : ActionBeancountMain,
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
            'Import from CSV': ActionImportAccountCsv,
            'Cancel': ActionMain
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
        if(self.action[CONFIRMATION_NAME]):
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
            'Import from CSV': ActionTransactionImportCsv,
            'Cancel': ActionMain
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
        TransactionImporter(Account.get_giro()).execute(self.path_name)


class ActionRuleMain(Action):

    def prompt(self) -> None:
        choices = {
            'Add Rule': ActionAddRule,
            'List Rules': ActionListRules,
            'Delete Rule': ActionDelRule,
            'Cancel': ActionMain
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
                'name': 'rule_description',
            }
        ])

        choices = [
            {
                'name' : 'Add Transformation',
                'value' : ActionCreateRuleTransformation
            },
            {
                'name' : 'Add Condition',
                'value' : ActionCreateCondition
            },
            {
                'name' : 'Done',
                'value' : None
            }
        ]

        self.action_results = []

        while 1:
            rule_action = cust_prompt(get_option_list(choices, "Configure action"))
            
            if 'option' not in rule_action:
                break
            
            action_class = rule_action['option']
            action_instance = action_class()
            action_instance.prompt()
            self.action_results.append(action_instance)

        self.execute()

    def execute(self) -> None:
        rule_params = self.action_rule
        action_results = self.action_results

        ref_objs = []

        for action_result in action_results:
            action_result.execute()
            ref_objs.append(action_result.ref_obj)

        Rule.build(rule_params['account_id'], rule_params['rule_description'], ref_objs=ref_objs)



class ActionCreateRuleTransformation(Action):

    TRANSACTION_ATTRIBUTES = [
        {
            'name' : 'partner account',
            'value' : 'partner_account_id'
        },
        {
            'name' : 'partner name',
            'value' : 'partner_name'
        }    
    ]

    def prompt(self) -> None:
        self.action = cust_prompt([
            get_option_list(ActionCreateRuleTransformation.TRANSACTION_ATTRIBUTES, "Choose transaction attribute to transform", 
                name='attribute_name'),
            input(name='attribute_value', message='Choose value'),
            get_datatype_list(name='value_type')
        ])

    def execute(self) -> None:
        self.ref_obj = RuleTransformation.build(**self.action)


class ActionCreateCondition(Action):

    CONDITION_TYPES = [
        {
            'name' : 'Regexp',
            'value' : ConditionRegexp
        },
        {
            'name' : 'Is Income',
            'value' : ConditionIsIncome
        },
        {
            'name' : 'Is Expense',
            'value' : ConditionIsExpense
        }    
    ]

    TRANSACTION_ATTRIBUTES = [
        {
            'name' : 'reference',
            'value' : 'reference'
        },
        {
            'name' : 'partner name',
            'value' : 'partner_name'
        }    
    ]

    def prompt(self) -> None:

        regexp_prompt_lambda = lambda answers: answers['condition_type'] == ConditionRegexp

        self.action = cust_prompt([
            get_option_list(ActionCreateCondition.CONDITION_TYPES, 'Choose condition type', 'condition_type'),
            input('regexp_pattern', 'Enter regexp', when=regexp_prompt_lambda),
            get_option_list(ActionCreateCondition.TRANSACTION_ATTRIBUTES, 'Choose transaction attribute', 'transaction_attribute',
                when=regexp_prompt_lambda)
        ])

    def execute(self) -> None:
        condition_class = self.action['condition_type']

        args = {k: v for (k, v) in self.action.items() if k != 'condition_type'}

        self.ref_obj = condition_class.build(**args)


class ActionListRules(Action):

    @returntomain
    def prompt(self) -> None:
        self.execute()

    def execute(self) -> None:
        rules = Rule.get_all()
        print("Rules: ")
        for rule in rules:
            print(f'  - {rule.get_as_string()}')


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


class ActionBeancountMain(Action):

    def prompt(self) -> None:
        choices = {
            'Extract': ActionBeancountExtract,
            'Cancel': ActionMain
        }

        cust_prompt_class_option(choices, 'choose option')


class ActionBeancountExtract(Action):

    @returntomain
    def prompt(self) -> None:
        self.action = cust_prompt([
            get_path('Save as', default=P_BEANCOUNT)
        ])
        self.execute()

    def execute(self) -> None:
        path = self.action[PATH_NAME]
        if not path.endswith(".beancount"):
            path = f'{path}.beancount'
        f = open(path, "w") 
        beancount_write_all(f)
        f.close()
        

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