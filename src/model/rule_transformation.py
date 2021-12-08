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

    _attribute_name = Column(String, nullable=False)

    attribute_value = Column(String)

    value_type = Column(String(8), default='str')

    rule = relationship('Rule', back_populates='rule_transformations')

    @hybrid_property
    def attribute_name(self):
        return self._attribute_name

    @attribute_name.setter
    def attribute_name(self, attribute_name):
        assert hasattr(Transaction, attribute_name)

        self._attribute_name = attribute_name
    