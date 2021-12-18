import os
from typing import List
from data_import.csv_importer import CsvImporter
from database import BaseModel, get_session

from model.account import Account
from model.rule import Rule
from model.transaction import Transaction
from config import Config

class TransactionImporter():

    #TODO config file
    

    def __init__(self, account_key) -> None:
        super().__init__()
        self.account_key = account_key

    def execute(self, filename : str):
        session = get_session()

        accounts = Account.get_full_account_dict(session)
        
        giro_account = accounts[self.account_key]

        rules : List[Rule] = session.query(Rule).filter(Rule.account_id==giro_account.id).all()

        transactions = CsvImporter().execute(filename, Transaction.build, Config.GIRO["TRANSACTION_MAPPING"])

        for transaction in transactions:
            transaction.account_id = giro_account.id
            for rule in rules:
                if rule.should_apply(transaction):
                    rule.transform(transaction)

        # find partners without account
        unassigned_transactions = [t for t in transactions if t.partner_account_id is None]

        session.add_all(transactions)
        session.commit()