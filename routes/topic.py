from functools import wraps

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.board import Board
from models.reply import Reply
from routes import current_user, new_csrf_token, login_required, csrf_required

from models.topic import Topic
from utils import log

main = Blueprint('topic', __name__)


def topic_same_user_required(route_function):
    @wraps(route_function)
    def f():
        u = current_user()

        if 'id' in request.args:
            topic_id = request.args.get('id', -1)
        else:
            topic_id = request.form.get('id', -1)

        t = Topic.one(id=topic_id)

        if u.id == t.user_id:
            return route_function()
        else:
            return redirect(url_for('.detail', id=t.id))

    return f


@main.route("/new")
@login_required
def new():
    bs = Board.all()
    t = new_csrf_token()
    return render_template(
        'topic/new.html',
        total_board=bs,
        csrf_token=t,
        token=t,
    )


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()

    form['user_id'] = u.id

    t = Topic.new(**form)

    return redirect(url_for('.detail', id=t.id))


@main.route('/<int:id>')
def detail(id):
    t = Topic.get(id)
    u = current_user()

    # 判断是否展示编辑栏
    if u is None:
        u_id = -1
        token = ''
    else:
        u_id = u.id
        token = new_csrf_token()

    return render_template(
        'topic/detail.html',
        topic=t,
        tpoic_user=t.user(),
        current_user_id=u_id,
        board=t.board(),
        token=token,
    )


@main.route("/delete")
@login_required
@topic_same_user_required
@csrf_required
def delete():
    id = request.args.get('id', -1)
    # 删除话题相对应的所有回复
    replies = Reply.all(topic_id=id)

    for r in replies:
        Reply.delete(r.id)

    # 删除话题
    Topic.delete(id=id)

    return redirect(url_for('index.index'))


@main.route("/edit")
@login_required
@topic_same_user_required
def edit():
    id = request.args.get('id', -1)

    t = Topic.one(id=id)

    bs = Board.all()

    token = new_csrf_token()

    return render_template(
        'topic/edit.html',
        topic=t,
        current_board_id=t.board_id,
        total_board=bs,
        token=token,
    )


@main.route("/update", methods=["POST"])
@login_required
@topic_same_user_required
@csrf_required
def update():
    form = request.form.to_dict()
    id = form.pop('id')

    t = Topic.update(id, **form)

    return redirect(url_for('.detail', id=t.id))
