from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    jsonify, json)

from models.user import User
from routes import current_user, login_required

from models.mail import Mail
from utils import log

main = Blueprint('mail', __name__)


@main.route('/')
@login_required
def index():
    u = current_user()

    sent_mails = Mail.all(sender_id=u.id)
    received_mails = Mail.all(receiver_id=u.id)

    return render_template(
        'mail/index.html',
        sent=sent_mails,
        received=received_mails,
        user=u
    )


@main.route('/new')
@login_required
def new():
    receiver_id = int(request.args.get('receiver_id'))
    receiver = User.one(id=receiver_id)
    u = current_user()
    return render_template('mail/new.html', user=u, receiver=receiver)


@main.route('/add', methods=['POST'])
@login_required
def add():
    form = request.form.to_dict()
    u = current_user()

    form['sender_id'] = u.id

    Mail.new(**form)

    return redirect(url_for('.index'))


@main.route('/datail')
@login_required
def view():
    id = int(request.args.get('id'))
    mail = Mail.one(id=id)
    u = current_user()

    if u.id in [mail.sender_id, mail.receiver_id]:
        return render_template('mail/detail.html', mail=mail)
    else:
        return redirect(url_for('.index'))

