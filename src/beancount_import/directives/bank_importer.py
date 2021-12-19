from beancount_import.directives.directive_importer import DirectiveImporter

from database import get_session
from model.transaction import Transaction

from beancount.core import data
from beancount.core.number import D
from beancount.core import amount as bc_amount
from beancount.core import flags


class BankImporter(DirectiveImporter):

    def __init__(self, account) -> None:
        self.account = account

    def build_directives(self, db_transactions):
        acc_name = lambda acc : f'{acc.account_type}:{acc.name}'
        to_amount = lambda am, curr : bc_amount.Amount(D(str(am)), curr)

        directives = []

        for db_transaction in db_transactions:

            acc = db_transaction.account
            acc_p = db_transaction.partner_account

            # TODO remove
            amount = float(db_transaction.amount.replace('.', '').replace(',', '.'))
            
            postings = [
                data.Posting(acc_name(acc), to_amount(amount, acc.currency), None, None, None, None),
                data.Posting(acc_name(acc_p), to_amount(-amount, acc_p.currency), None, None, None, None)
            ]

            transaction = data.Transaction(
                # TODO add filename 
                meta = data.new_metadata('f', db_transaction.id),
                date = db_transaction.date,
                flag = flags.FLAG_OKAY, # TODO eventually add transformation
                payee = db_transaction.partner_name, 
                narration = db_transaction.reference,
                tags = set(),
                links = set(),
                postings = postings
            )
            directives.append(transaction)

        return directives
                
    def extract(self):
        session = get_session()

        db_transactions = session.query(Transaction).filter(Transaction.account_id==self.account.id 
                            and Transaction.partner_account_id is not None).all()
        directives = self.build_directives(db_transactions)

        return directives
