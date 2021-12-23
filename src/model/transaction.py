from typing import List

from beancount.core import amount
from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.orm import relationship
from evaluation.text_similarity import get_similarity_measure
from model.account import Account
from database import BaseModel, get_session, sessioncommit
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
    
    def get_most_similar_transactions(self, transactions : List, n=1) -> List:
        def as_str(transaction):
            # TODO refine - eventually consider partner name
            return transaction.reference

        transactions_as_str = [as_str(t) for t in transactions]
        idx = get_similarity_measure(as_str(self), transactions_as_str)
        # TODO n transactions
        return [transactions[idx]]

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

    @staticmethod
    def get_unassigned_transactions():
        session = get_session()

        return session.query(Transaction).filter(Transaction.partner_account_id == None).all()

    def __str__(self) -> str:
        return f'{self.account.key} -> {self.partner_account.key} | {self.amount} {self.currency_code} | {self.reference}'