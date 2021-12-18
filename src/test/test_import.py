import csv
import unittest

from data_import.bank_importer import TransactionImporter
from config import config_by_name
from model.account import Account
from model.transaction import Transaction
import os

from database import get_session, sessioncommit
from test.util import testdb


class TestGiroImporter(unittest.TestCase):

    GIRO_ACCOUNT_KEY = 'TEST_GIRO'

    @testdb
    @sessioncommit
    def setUp(self) -> None:
        # required db objects
        return [
            Account(account_type='Expenses', name='test', key=TestGiroImporter.GIRO_ACCOUNT_KEY)
        ]
    
    def test_import(self):

        session = get_session()

        file = '/workspaces/beancount-cli/data/test/giro_transaction_test.csv'
        
        importer = TransactionImporter(TestGiroImporter.GIRO_ACCOUNT_KEY)
        
        importer.execute(file)

        transactions = session.query(Transaction).all()

        with open(file) as csvDataFile:
            reader = csv.reader(csvDataFile)

            columns = next(reader)

            rows = [r for r in reader]

            self.assertEqual(len(rows), len(transactions))
