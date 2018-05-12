from sqlalchemy import Column, String

from models import SQLMixin, SQLBase


class Board(SQLMixin, SQLBase):
    __tablename__ = 'Board'
    """
    Board 是一个保存板块的 model
    现在只有一个属性 title
    """
    title = Column(String(100), nullable=False)

