from __future__ import annotations
from typing import DefaultDict, List

from sqlalchemy import Column, Integer
from sqlalchemy import orm
from sqlalchemy.orm import immediateload, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, String

from database import BaseModel, get_session
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

    @classmethod
    def build(cls, account_id, rule_description, ref_objs : List):

        session = get_session()

        rule = cls()
        rule.account_id = account_id
        rule.rule_description = rule_description

        session.add(rule)
        session.flush()

        for ref_obj in ref_objs:
            ref_obj.rule_id = rule.id

        session.add_all(ref_objs)
        session.commit()

        return rule

    @staticmethod
    def get_all(order_by_criterion = None):
        if order_by_criterion is None:
            order_by_criterion = [Rule.account_id, Rule.rule_description]

        session = get_session()
        return session.query(Rule).order_by(*order_by_criterion).all()

    def get_as_string(self, indentation_size=2, indentation_start=4):

        indentation_size_lvl_2 = indentation_start + indentation_size
        
        indentation_lvl_1 = ' ' * indentation_start
        indentation_lvl_2 = ' ' * indentation_size_lvl_2

        conditions_str = '\n{indentation_lvl_2}'.join([condition.get_as_string(indentation_size, indentation_size_lvl_2) for condition in self.conditions]) 
        transformations_str = '\n{indentation_lvl_2}'.join([transformation.get_as_string(indentation_size, indentation_size_lvl_2) for transformation in self.rule_transformations]) 

        conditions = f'\n{indentation_lvl_1}Conditions:\n{conditions_str}'
        transformations = f'\n{indentation_lvl_1}Transformations:\n{transformations_str}'
        return f'[{self.account.key}] {self.rule_description}{conditions}{transformations}' 
        