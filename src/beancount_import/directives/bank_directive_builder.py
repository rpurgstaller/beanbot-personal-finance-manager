from typing import List
from beancount_import.directives.bank_directive_builder import BaseDirectiveBuilder
from model.transaction import DbTransaction

from beancount.core import data
from beancount.core.number import D
from beancount.core import amount
from beancount.core import flags

from model.transaction import Transaction


class BankDirectiveBuilder(BaseDirectiveBuilder):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._directives = []

    @property
    def directives(self) -> List:
        directives = self._directives
        self.reset()
        return directives

    def build_directives(self, db_transactions : List[Transaction], filename):
        acc_name = lambda acc : f'{acc.account_type}:{acc.name}'
        to_amount = lambda x : amount.Amount(D(str(x)))

        for db_transaction in db_transactions:

            acc = db_transaction.account
            acc_p = db_transaction.partner_account
            
            postings = [
                data.Posting(acc_name(acc), to_amount(db_transaction.amount), acc.currency, None, None, None, None),
                data.Posting(acc_name(acc_p), to_amount(-db_transaction.amount), acc_p.currency, None, None, None, None)
            ]

            transaction = data.Transaction(
                meta = data.new_metadata(filename, db_transaction.id),
                date = db_transaction.date,
                flag = flags.FLAG_OKAY, # TODO eventually add transformation
                payee = db_transaction.payee, 
                narration = db_transaction.reference,
                tags = set(),
                links = set(),
                postings = postings
            )
            self._directives.append(transaction)

        return self

