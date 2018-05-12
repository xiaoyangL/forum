from sqlalchemy import Column, String

from models import reset_database, SQLMixin, SQLBase, configured_engine
from models.board import Board
from models.mail import Mail
from models.reply import Reply
from models.topic import Topic
from models.user import User


def main():
    reset_database()


if __name__ == '__main__':
    main()
