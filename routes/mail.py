from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user

from models.mail import Mail
from utils import log

main = Blueprint('mail', __name__)


@main.route('/add', methods=['POST'])
def add():
    form = request.form.to_dict()
    u = current_user()

    form['sender_id'] = u.id
    Mail.new(**form)

    return redirect(url_for('.index'))


@main.route('/')
def index():
    u = current_user()
    sent_mails = Mail.all(sender_id=u.id)
    received_mails = Mail.all(receiver_id=u.id)
    return render_template(
        'mail/index.html',
        sent=sent_mails,
        received=received_mails,
    )


@main.route('/datail/<int:id>')
def view(id):
    mail = Mail.one(id=id)
    u = current_user()

    if u.id in [mail.sender_id, mail.receiver_id]:
        return render_template('mail/detail.html', mail=mail)
    else:
        return redirect(url_for('.index'))


