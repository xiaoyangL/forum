import time
import config
from utils import log

from sqlalchemy import create_engine, Column, Integer, Boolean, literal, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


def configured_engine():
    url = 'mysql+pymysql://root:{}@localhost/web?charset=utf8mb4'.format(
        config.mysql_password
    )
    e = create_engine(url, echo=True)
    return e


SQLBase = declarative_base()


def reset_database():
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(
        config.mysql_password
    )
    # print('sql url', url)
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS web')
        c.execute('CREATE DATABASE web CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE web')

    SQLBase.metadata.create_all(bind=e)


class SQLMixin(object):
    session = scoped_session(sessionmaker(bind=configured_engine()))
    query = session.query_property()

    id = Column(Integer, primary_key=True)
    deleted = Column(Boolean, nullable=False, default=False)
    created_time = Column(Integer, nullable=False)
    updated_time = Column(Integer, nullable=False)

    def add_default_value(self):
        timestamp = int(time.time())
        self.created_time = timestamp
        self.updated_time = timestamp

    @classmethod
    def new(cls, **kwargs):
        m = cls()
        # User.id = id
        for name, value in kwargs.items():
            setattr(m, name, value)
        m.add_default_value()

        SQLMixin.session.add(m)
        SQLMixin.session.commit()
        return m

    @classmethod
    def delete(cls, id):
        cls.update(id, deleted=True)

    @classmethod
    def update(cls, id, **kwargs):
        m = cls.query.filter_by(id=id).first()
        for name, value in kwargs.items():
            setattr(m, name, value)
        m.updated_time = int(time.time())

        SQLMixin.session.add(m)
        SQLMixin.session.commit()
        return m

    @classmethod
    def all(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    @classmethod
    def one(cls, **kwargs):
        m = cls.query.filter_by(**kwargs).first()
        return m

    @classmethod
    def exist(cls, **kwargs):
        # windows 下 literal(True) 有 bug
        e = exists()

        for name, value in kwargs.items():
            e = e.where(getattr(cls, name) == value)

        r = cls.session.query(e).scalar()
        log("eeeeeeeeeee: ", r)
        return r

    def __repr__(self):
        s = ''
        for attr, column in self.__mapper__.c.items():
            if hasattr(self, attr):
                v = getattr(self, attr)
                s += '{}: ({})\n'.format(attr, v)
        return '< {}\n{} >\n'.format(self.__class__.__name__, s)
