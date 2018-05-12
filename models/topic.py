import time
from models import Model
from models.user import User
from models.reply import Reply

from sqlalchemy import Column, String, Integer, Text
from models import SQLMixin, SQLBase


class Topic(SQLMixin, SQLBase):
    __tablename__ = 'Topic'
    """
    Topic 是一个保存帖子的 model
    现在只有5个属性 title、content、views、user_id和board_id
    """
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    views = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, nullable=False)
    board_id = Column(Integer, nullable=False, default=-1)

    @classmethod
    def get(cls, id):
        t = cls.one(id=id)

        t.views += 1
        cls.update(t.id, views=t.views)
        return t

    def user(self):
        from .user import User
        u = User.one(id=self.user_id)
        return u

    def replies(self):
        from .reply import Reply
        ms = Reply.all(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count

    def board(self):
        from .board import Board
        b = Board.one(id=self.board_id)
        return b
