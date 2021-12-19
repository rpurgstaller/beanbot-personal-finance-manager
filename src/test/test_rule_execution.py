import unittest

from data_import.bank_importer import TransactionImporter
from config import config_by_name
from model.account import Account
import os
from datetime import datetime

from database import get_session, sessioncommit
from model.condition import Condition, ConditionRegexp
from model.rule import Rule
from model.rule_transformation import RuleTransformation
from model.transaction import Transaction
from test.util import testdb


class TestRule(unittest.TestCase):

    GIRO_ACCOUNT_KEY = 'TEST_GIRO'

    @testdb
    def setUp(self) -> None:
        pass
    
    def test_giro_execution(self):
        session = get_session()
        
        # Create accounts
        acc_transaction = Account(account_type='Expenses', name='Test:SomeExpense', key="TEST_EXP")
        acc_partner = Account(account_type='Income', name='Test:SomeIncome', key="TEST_INC")
        session.add_all([acc_transaction, acc_partner])
        session.flush()

        # transactions
        file = '/workspaces/beancount-cli/data/test/giro_transaction_test.csv'

        # Create Rule, transformation and conditions
        def create_rule(acc : Account, rule_desc : str, rule_transformation_attr_name : str, rule_transformation_attr_value : str,
                condition_transaction_attribute : str, condition_regexp : str):
            rule = Rule(account_id=acc.id, rule_description=rule_desc)
            session.add(rule)
            session.flush()
            condition = ConditionRegexp(rule_id=rule.id, regexp_pattern=condition_regexp, transaction_attribute=condition_transaction_attribute)
            rule_transformation = RuleTransformation(rule_id=rule.id, attribute_name=rule_transformation_attr_name, 
                    attribute_value=rule_transformation_attr_value)
            session.add_all([rule_transformation, condition])

        create_rule(acc_transaction, 'match', 'partner_account_id', acc_partner.id, 'partner_name', '^sUpeRmArket')
        create_rule(acc_transaction, 'no_match', 'partner_bic', "1234567", 'reference', '^NoMatch')

        session.commit()

        TransactionImporter(Account.get_giro()).execute(file)

        transactions = session.query(Transaction).filter(Transaction.partner_name == 'supermarket').all()

        for transaction in transactions:
            self.assertIsNotNone(transaction)
            self.assertEqual(transaction.partner_account_id, acc_partner.id)
            self.assertFalse(transaction.partner_bic)




