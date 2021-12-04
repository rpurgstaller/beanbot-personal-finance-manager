from beancount.core import amount
from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.orm import relationship
from model.account import DbAccount
from database import DbBaseModel, get_session, sessioncommit
from sqlalchemy.sql.schema import ForeignKey


class DbPartner(DbBaseModel):
    __tablename__ = 'partner'

    partner_name = Column(String, nullable=False)
    partner_iban = Column(String)
    partner_bic = Column(String)
    partner_account_number = Column(String)
    partner_bank_code = Column(String)

    account_id = Column(Integer, ForeignKey(DbAccount.id))
    
    account = relationship('DbAccount', foreign_keys='DbPartner.account_id')
    
    @classmethod
    @sessioncommit
    def build_and_assign(cls, name, iban, bic, account, bank_code, reference):
        session = get_session()

        # TODO assign according to the rule engine
        partner = session.query(DbPartner).filter(DbPartner.name == name and DbPartner.iban == iban and DbPartner.account == account)
        
        if partner:
            return partner

        partner = cls()
        partner.name = name
        partner.iban = iban
        partner.bic = bic
        partner.account = account
        partner.bank_code = bank_code

        return partner


