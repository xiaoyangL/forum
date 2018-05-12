import hashlib

from sqlalchemy import Column, String, Text

from models import SQLMixin, SQLBase
from utils import log


class User(SQLMixin, SQLBase):
    __tablename__ = 'User'
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False, default='/images/1.jpg')
    signature = Column(Text, default="这家伙很懒，什么个性签名都没有留下。")

    @staticmethod
    def salted_password(password, salt='?+=jioat10][auihi}/;;'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    def add_default_value(self):
        super().add_default_value()
        self.password = User.salted_password(self.password)

    @classmethod
    def register(cls, form):
        name = form['username']
        password = form['password']
        if len(name) > 2 and len(password) > 2 and not User.exist(username=name):
            u = User.new(**form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        form['password'] = User.salted_password(form['password'])
        e = User.exist(**form)
        if e:
            return User.one(**form)
        else:
            return None

    def recent_created_topics(self):
        """返回最近创建的话题"""
        from .topic import Topic
        topics = Topic.all(user_id=self.id, deleted=False)

        # 按时间倒序
        topics = sorted(
            topics,
            key=lambda topic: topic.created_time,
            reverse=True
        )
        return topics

    def recent_join_topics(self):
        """返回最近参与的话题"""
        from models.reply import Reply
        from models.topic import Topic
        topics = Topic.all(user_id=self.id, deleted=False)

        # 最近的回复
        replies = sorted(
            Reply.all(user_id=self.id, deleted=False),
            key=lambda repliy: repliy.updated_time,
            reverse=True
        )

        # 找到最近回复相对应的话题
        join_topics = [Topic.one(id=r.topic_id, deleted=False) for r in replies]

        # 去掉重复的话题
        processed = {}
        for t in join_topics:
            processed[t.id] = t

        join_topics = []
        for topic in processed.values():
            join_topics.append(topic)

        return join_topics
