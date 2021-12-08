import re
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.orm.collections import attribute_mapped_collection, collection
from sqlalchemy.sql.schema import ForeignKey
from database import BaseModel 
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import String


class Condition(BaseModel):
    __tablename__ = 'conditions'

    rule_id = Column(Integer, ForeignKey('rules.id'))

    condition_type = Column(String(50))
    
    __mapper_args__ = {
        'polymorphic_on':condition_type,
        'polymorphic_identity':'rules'
    }
    
    rule = relationship('Rule', foreign_keys='Condition.rule_id')
    
    def evaluate(self, transaction) -> None:
        pass


class ConditionRegexp(Condition):

    regexp_pattern = Column(String, nullable=False)

    transaction_attribute = Column(String, nullable=False)

    __mapper_args__ = { 'polymorphic_identity' : 'condition_regexp' }

    def evaluate(self, transaction) -> bool:        
        regexp_string = getattr(transaction, self.transaction_attribute)
        if regexp_string is None:
            return False

        return re.search(self.regexp_pattern, regexp_string, re.IGNORECASE)


class ConditionIsIncome(Condition):

    __mapper_args__ = { 'polymorphic_identity' : 'condition_is_income' }

    def evaluate(self, transaction) -> bool:
        return transaction.amount > 0


class ConditionIsExpense(Condition):

    __mapper_args__ = { 'polymorphic_identity' : 'condition_is_expense' }

    def evaluate(self, transaction) -> bool:
        return transaction.amount < 0

        