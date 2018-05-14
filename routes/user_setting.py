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
from routes import current_user, login_required
from utils import log

main = Blueprint('setting', __name__)


@main.route('/')
@login_required
def setting_view():
    u = current_user()
    return render_template('user/setting.html', user=u)


@main.route('/process', methods=['POST'])
@login_required
def process_setting():
    form = request.form.to_dict()

    u = current_user()
    User.update(u.id, **form)

    flash('保存成功。')
    return redirect(url_for('.setting_view', user=u))


@main.route('/image/add', methods=['POST'])
@login_required
def image_add():
    file = request.files['avatar']

    # 转换图片名字，以防攻击
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    # 更新user.image属性
    u = current_user()
    image_path = '/images/{}'.format(filename)
    User.update(u.id, image=image_path)

    flash('头像修改成功')

    return redirect(url_for('.setting_view'))


@main.route('/modify/password', methods=['POST'])
@login_required
def modify_password():
    old_password = request.form.get('old_password', '')
    u = current_user()

    if User.salted_password(old_password) == u.password:

        new_password = request.form.get('new_password', '')
        new_password = User.salted_password(new_password)

        User.update(u.id, password=new_password)
        flash('密码修改成功。')
    else:
        flash('当前密码不正确。')

    return redirect(url_for('.setting_view', user=u))



