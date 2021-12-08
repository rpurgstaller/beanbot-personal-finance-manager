from __future__ import annotations
from typing import DefaultDict

from sqlalchemy import Column, Integer
from sqlalchemy import orm
from sqlalchemy.orm import immediateload, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, String

from database import BaseModel
from model.transaction import Transaction
from mixins.param_dict_mixin import ParamDictMixin
from model.condition import Condition
from model.rule_transformation import RuleTransformation


class Rule(BaseModel):

    __tablename__ = 'rules'

    PARAM_KEY_TARGET_ACCOUNT = 'target_account'
    
    account_id = Column(Integer, ForeignKey('accounts.id'))

    rule_description = Column(String(256))
    
    account = relationship('Account', foreign_keys='Rule.account_id')

    rule_transformations = relationship('RuleTransformation', back_populates='rule')

    conditions = relationship('Condition', back_populates='rule')

    def should_apply(self, transaction : Transaction):
        return all(map(lambda c: c.evaluate(transaction), self.conditions))

    def transform(self, transaction : Transaction):
        for rule_transformation in self.rule_transformations:
            setattr(transaction, rule_transformation.attribute_name, rule_transformation.attribute_value)


