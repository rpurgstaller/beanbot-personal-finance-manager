import unittest
from data_import.bank_importer import GiroImporter
from config import config_by_name
from model.account import DbAccount

import src.database as db

class TestGiroImporter(unittest.TestCase):

    def setUp(self) -> None:
        cfg = config_by_name['test']()
        db.create(cfg.DB_FILENAME)
        session = db.get_session()
        session.add(DbAccount(account_type='Expenses', name='test', key='test'))
    
    def test_import():
        importer = GiroImporter('/workspaces/beancount-cli/data/test/gio')
        importer.execute()