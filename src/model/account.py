from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql.expression import false

from database import DbBaseModel, get_session, sessioncommit


class DbAccount(DbBaseModel):

    __tablename__ = 'accounts'

    #id = Column(Integer, primary_key=True)
    account_type = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=False)

    key = Column(String, nullable=False)

    currency = Column(String, default='EUR')

    def get_full_name(self) -> str:
        return f'{self.account_type}:{self.name}'

    @classmethod
    def build(cls, account_type, name, key, currency='EUR'):
        account = cls()
        account.account_type = account_type
        account.name = name
        account.key = key
        return account

    @staticmethod
    def get_full_account_dict(session):
        return {a.key : a for a in session.query(DbAccount).all()}

    @staticmethod
    def get_all():
        return get_session().query(DbAccount).all()

    def __str__(self) -> str:
        return f'[{self.key}] {self.get_full_name()}'