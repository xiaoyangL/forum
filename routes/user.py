import os
import uuid
from datetime import timedelta

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory,
    flash
)

from models.user import User
from routes import current_user
from utils import log

main = Blueprint('user', __name__)


@main.route("/register/view")
def register_view():
    return render_template("user/register.html")


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    u = User.register(form)
    return redirect(url_for('.login_view'))


@main.route("/login/view")
def login_view():
    return render_template("user/login.html")


@main.route("/login", methods=['POST'])
def login():
    form = request.form.to_dict()
    u = User.validate_login(form)

    if u is not None:
        session['user_id'] = u.id
        session.permanent_session_lifetime = timedelta(days=31)

        return redirect(url_for('index.index'))
    else:
        flash('登录失败，用户或密码有误')
        return redirect(url_for('.login_view'))


@main.route('/profile')
def profile():
    u = current_user()
    # 如果没有传user的id那么就访问自己的主页
    user_id = int(request.args.get('id', u.id))

    if u.id == user_id:
        user = u
    else:
        user = User.one(id=user_id)

    recent_created_topics = user.recent_created_topics()
    recent_join_topics = user.recent_join_topics()

    return render_template(
        'user/profile.html',
        user=user,
        recent_created_topics=recent_created_topics,
        recent_join_topics=recent_join_topics,
    )

