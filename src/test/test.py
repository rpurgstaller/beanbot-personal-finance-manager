import unittest
from config import config_by_name
import database as db
from data_import.bank_importer import GiroImporter


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cfg = config_by_name['test']()

        db.create(cfg.DB_FILENAME)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

class TestGiroImporter(unittest.TestCase):
    
    def test_import(self):
        importer = GiroImporter()
        importer.execute('/workspaces/beancount-cli/data/test/giro_transaction_test.csv')


if __name__ == '__main__':
    unittest.main()