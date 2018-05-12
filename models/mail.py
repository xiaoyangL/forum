from sqlalchemy import Column, String, Integer, Text

from models import SQLMixin, SQLBase


class Mail(SQLMixin, SQLBase):
    __tablename__ = 'Mail'
    """
    Mail 是一个保存用户私信的 model
    现在只有四个属性 title、content、sender_id和receiver_id
    """
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
