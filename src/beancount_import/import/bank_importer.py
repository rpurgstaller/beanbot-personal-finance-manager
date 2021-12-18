import re
import os

from beancount.ingest import importer
from sqlalchemy.engine.base import Transaction

from database import get_session
from model.account import Account
from beancount_import.directives.bank_directive_builder import BankDirectiveBuilder

class BankImporter(importer.ImporterProtocol):

    def __init__(self, account_key, lastfour, filename_pattern, file_extension) -> None:
        self.account_key = account_key
        self.lastfour = lastfour
        self.filename_pattern = filename_pattern
        self.file_extension = file_extension

    def identify(self, file):
        return re.match(self.filename_pattern + '.' + self.file_extension, os.path.basename(file.name))
        
    def extract(self, file):
        session = get_session()

        account = session.query(Account).filter(Account.key==self.account_key).first()
        db_transactions = session.query(Transaction).filter(Transaction.account_id==account.id).all()
        directives = BankDirectiveBuilder().build_directives(db_transactions, file.name).directives

        session.close()

        return directives
