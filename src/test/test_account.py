import unittest
from config import config_by_name
from model.account import Account
import os

from database import get_session, sessioncommit
from test.util import testdb


class TestAccount(unittest.TestCase):

    GIRO_ACCOUNT_KEY = 'TEST_GIRO'

    @testdb
    def setUp(self) -> None:
        # required db objects
        pass
    
    def test_create(self):
        session = get_session()
        objs = [
            Account(account_type='Expenses', name='Test:SomeExpense', key="TEST_EXP"),
            Account(account_type='Income', name='Test:SomeIncome', key="TEST_INC")
        ]
        session.add_all(objs)
        session.commit()

        accounts = Account.get_all()
        self.assertEqual(len(objs), len(accounts))
        
        for obj in objs:
            self.assertIn(obj, accounts)

            



        

        