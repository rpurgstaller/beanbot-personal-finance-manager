from abc import ABC, abstractmethod

from PyInquirer import prompt


def returntomain(func):
    def wrap(*args, **kwargs):
        func(*args, **kwargs)
        ActionMain().execute()
    return wrap


class Action(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass

    @classmethod
    def build(cls, **kwargs):

        return cls(**kwargs)


class ActionMain(Action):

    def execute(self) -> str:
        choices = {
            'Add account': ActionAddAccount,
            'Import transactions': ActionImportTransactions,
            'pizza': ActionPizza,
            'exit': ActionExit
        }

        action = prompt([
            {
                'type': 'rawlist',
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
        print('Execute: Add Account ')


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