import unittest
from config import config_by_name
import database as db
from data_import.bank_importer import TransactionImporter


def testdb(func):
    def wrap(*args, **kwargs):
        cfg = config_by_name['test']()
        db.initialize_and_reset(cfg.DB_FILENAME)

        return func(*args, **kwargs)
    return wrap
    

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cfg = config_by_name['test']()

        db.create(cfg.DB_FILENAME)

    @classmethod
    def tearDownClass(cls) -> None:
        pass



if __name__ == '__main__':
    unittest.main()