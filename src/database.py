from typing import Iterable
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session

from util.path import DB_PATH


Model = declarative_base()
_engine = create_engine(f'sqlite:///{DB_PATH}/model.db')
_session = None


def get_session():
    global _session
    if _session is None:
        _session = Session(_engine)
    
    return _session

def reset():
    metadata = MetaData()
    metadata.reflect(bind=_engine)
    Model.metadata.drop_all(_engine, metadata.tables.values(), checkfirst=True)


def create():
    metadata = MetaData()
    metadata.reflect(bind=_engine)
    Model.metadata.create_all(_engine)


def reset_and_create():
    reset()
    create()
    

def sessioncommit(func):
    def wrap(*args, **kwargs):
        session = get_session()
        obj = func(*args, **kwargs)

        if isinstance(obj, Iterable):
            session.add_all(obj)
        else:
            session.add(obj)
            
        session.commit()
    return wrap


class DbBaseModel(Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, onupdate=func.now())

    @classmethod
    def build(cls):
        pass

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    @classmethod
    def delete_by_id(cls, id : int):
        session = get_session()
        session.query(cls).filter(cls.id == id).delete(synchronize_session=False)
        session.commit()
