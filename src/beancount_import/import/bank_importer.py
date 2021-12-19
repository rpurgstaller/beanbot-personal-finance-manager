import re
import os

from beancount.ingest import importer
from sqlalchemy.engine.base import Transaction

from database import get_session
from model.account import Account
from beancount_import.directives.bank_directive_builder import BankDirectiveBuilder

class BankImporter():

    def __init__(self, account) -> None:
        self.account = account
                
    def extract(self, file):
        session = get_session()

        db_transactions = session.query(Transaction).filter(Transaction.account_id==self.account.id).all()
        directives = BankDirectiveBuilder().build_directives(db_transactions, file.name).directives

        return directives
