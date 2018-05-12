import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory, flash)

from models.board import Board
from models.topic import Topic
from models.user import User
from routes import current_user

main = Blueprint('index', __name__)


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))

    if board_id == -1:
        ts = Topic.all(deleted=False)
    else:
        ts = Topic.all(board_id=board_id, deleted=False)

    bs = Board.all()

    u = current_user()

    if u is None:
        user = User()
        user.id = -1
    else:
        user = u

    return render_template(
        'topic/index.html',
        boards=bs,
        topics=ts,
        user=user
    )


@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)


# def blueprint():
#     main = Blueprint('index', __name__)
#     main.route("/")(index)
#     main.route("/register", methods=['POST'])(register)
#     main.route("/login", methods=['POST'])(login)
#     main.route('/profile')(profile)
#     main.route('/user/<int:id>')(user_detail)
#
#     return main
