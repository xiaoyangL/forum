from sqlalchemy import Column, Integer, Text

from models import SQLMixin, SQLBase


class Reply(SQLMixin, SQLBase):
    __tablename__ = 'Reply'
    """
    Reply 是一个保存帖子回复的 model
    现在只有2个属性 content、topic_id和user_id
    """
    topic_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False)

    def user(self):
        from .user import User
        u = User.one(id=self.user_id)
        return u
