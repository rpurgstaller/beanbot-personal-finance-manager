from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql.expression import false
from data_import.csv_importer import CsvImporter

from database import DbBaseModel, get_session, sessioncommit


class DbAccount(DbBaseModel):

    __tablename__ = 'accounts'

    account_type = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=False)
    key = Column(String, nullable=False, unique=True)
    currency = Column(String, default='EUR')

    def get_full_name(self) -> str:
        return f'{self.account_type}:{self.name}'

    @staticmethod
    @sessioncommit
    def build_from_file(filename):
        return CsvImporter().execute(filename, DbAccount.build)

    @classmethod
    @sessioncommit
    def build(cls, account_type, name, key, currency='EUR'):
        account = cls()
        account.account_type = account_type
        account.name = name
        account.key = key
        account.currency = currency
        return account

    @staticmethod
    def get_full_account_dict(session):
        return {a.key : a for a in session.query(DbAccount).all()}

    @staticmethod
    def get_all(order_by_criterion = None):
        if order_by_criterion is None:
            order_by_criterion = [DbAccount.account_type.asc(), DbAccount.name.asc()]

        s = get_session()
        return s.query(DbAccount).order_by(*order_by_criterion).all()

    def __str__(self) -> str:
        return f'[{self.key}] {self.get_full_name()}'