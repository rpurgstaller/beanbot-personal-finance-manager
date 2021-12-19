from beancount.core import amount
from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.orm import relationship
from model.account import Account
from database import BaseModel, sessioncommit
from sqlalchemy.sql.schema import ForeignKey
from dateutil.parser import parse as parse_date


class Transaction(BaseModel):
    __tablename__ = 'transactions'

    date = Column(Date, nullable=False)
    amount = Column(Integer, nullable=False)
    currency_code = Column(String, nullable=False, default="EUR")
    reference = Column(String, nullable=False)
    partner_name = Column(String, nullable=False)
    partner_iban = Column(String)
    partner_bic = Column(String)
    partner_account_number = Column(String)
    partner_bank_code = Column(String)
    
    account_id = Column(Integer, ForeignKey(Account.id), nullable=False)
    partner_account_id = Column(Integer, ForeignKey(Account.id))

    account = relationship('Account', foreign_keys='Transaction.account_id')
    partner_account = relationship('Account', foreign_keys='Transaction.partner_account_id')
    
    @classmethod
    def build(cls, date, amount, currency_code, reference, partner_name, partner_iban, partner_bic, partner_account_number, partner_bank_code):
        transaction = cls()
        transaction.date = parse_date(date)
        # TODO transform amount
        transaction.amount = amount
        transaction.currency_code = currency_code
        transaction.reference = reference
        transaction.partner_name = partner_name
        transaction.partner_iban = partner_iban
        transaction.partner_bic = partner_bic
        transaction.partner_account_number = partner_account_number
        transaction.partner_bank_code = partner_bank_code
        return transaction