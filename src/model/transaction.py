from beancount.core import amount
from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.orm import relationship
from model.account import DbAccount
from database import DbBaseModel, sessioncommit
from model.partner import DbPartner
from sqlalchemy.sql.schema import ForeignKey


class DbTransaction(DbBaseModel):
    __tablename__ = 'transactions'

    date = Column(Date, nullable=False)

    partner_id = Column(Integer, ForeignKey(DbPartner.id))

    account_id = Column(Integer, ForeignKey(DbAccount.id), nullable=False)

    reference = Column(String, nullable=False)

    account = relationship('DbAccount', foreign_keys='DbTransaction.account_id')

    partner = relationship('DbPartner', foreign_keys='DbTransaction.partner_id')
    
    
    @classmethod
    @sessioncommit
    def build(cls):
        pass