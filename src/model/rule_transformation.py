from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from database import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import Column

from mixins.key_value_mixin import KeyValueMixin
from model.transaction import Transaction

class RuleTransformation(BaseModel, KeyValueMixin):
    __tablename__ = 'rule_transformations'

    rule_id = Column(Integer, ForeignKey('rules.id'))

    attribute_name = Column(String, nullable=False)

    attribute_value = Column(String)

    value_type = Column(String(8), default='str')

    rule = relationship('Rule', back_populates='rule_transformations')

    @classmethod
    def build(cls, attribute_name, attribute_value, value_type):
        rule_transformation = cls()
        rule_transformation.attribute_name = attribute_name
        rule_transformation.attribute_value = attribute_value
        rule_transformation.value_type = value_type
        return rule_transformation
    
    def get_as_string(self, indentation_size=2, indentation_start=4) -> str:
        indentation_lvl_1 = ' ' * indentation_start
        return f'Attribute Name: {indentation_lvl_1}{self.attribute_name} - Attribute value: {self.attribute_value} ({self.value_type})'