from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session




Model = declarative_base()
_engine = create_engine('sqlite:////workspaces/beancount-cli/data/database/model.db')
_session = None


def get_session():
    global _session
    if _session is None:
        _session = Session(_engine)
    
    return _session


def execute_script(filepath : str):
    with _engine.connect() as con:
        with open(filepath, 'r') as file:

            session = get_session()

            text = file.read()

            statements = text.replace('\n', '').split(';')

            for stmt in statements:
                try:
                    con.execute(stmt)
                except Exception as e:
                    print(f'Unable to execute statement \'{stmt}\' in file \'{os.path.basename(filepath)}\', ERR: {e}')


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
        session.add(obj)
        session.commit()
    return wrap


class DbBaseModel(Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, onupdate=func.now())

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


