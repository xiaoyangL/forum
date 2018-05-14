import uuid
from functools import wraps

from flask import session, request, abort, redirect, url_for

from models.user import User
from utils import log


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 None
    # 然后 User.one来用 id 找用户
    # 找不到就返回 None
    if 'user_id' in session:
        uid = int(session['user_id'])
        e = User.exist(id=uid)
        if e:
            return User.one(id=uid)
        else:
            return None
    else:
        return None


def login_required(route_function):
    # 登录验证
    @wraps(route_function)
    def f():
        u = current_user()

        if u is None:
            return redirect(url_for('user.login_view'))
        else:
            return route_function()
    return f


csrf_tokens = dict()


def csrf_required(f):
    # csrf防御
    @wraps(f)
    def wrapper(*args, **kwargs):

        if 'token' in request.args:
            token = request.args.get('token')
        else:
            token = request.form.get('token')

        u = current_user()

        if token in csrf_tokens and csrf_tokens[token] == u.id:
            csrf_tokens.pop(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    # 生成随机字符串
    u = current_user()
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    return token
