from typing import Iterable
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import session
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session, sessionmaker

from util.path import DB_PATH


Model = declarative_base()
_database = None

def get_session():
    assert _database is not None, "Database is not initialized"
    return _database.session


def _init_db(db_filename):
    global _database
    _database = DB()
    _database.initialize(db_filename)


def initialize_db(db_filename):
    _init_db(db_filename)
    _database.create_all()


def initialize_and_reset(db_filename):
    _init_db(db_filename)
    _database.reset_and_create()


def sessioncommit(func):
    def wrap(*args, **kwargs):
        session = get_session()
        obj = func(*args, **kwargs)

        if isinstance(obj, Iterable):
            session.add_all(obj)
        else:
            session.add(obj)
            
        session.commit()
        return obj
    return wrap


class DB:

    def __init__(self) -> None:
        self._session = None

    def initialize(self, db_filename):
        self._engine = create_engine(f'sqlite:///{DB_PATH}/{db_filename}')

    def create_all(self):
        assert self._engine is not None, "Engine is not initialized"

        metadata = MetaData()
        metadata.reflect(bind=self._engine)
        Model.metadata.create_all(self._engine)

    def reset(self):
        assert self._engine is not None, "Engine is not initialized"

        metadata = MetaData()
        metadata.reflect(bind=self._engine)
        Model.metadata.drop_all(self._engine, metadata.tables.values(), checkfirst=True)
    
    def reset_and_create(self):
        self.reset()
        self.create_all()
    
    @property
    def session(self):
        if self._session is None:
            Session = sessionmaker(bind=self._engine)
            self._session = Session()

        return self._session


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
