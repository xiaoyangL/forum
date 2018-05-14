from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.board import Board


main = Blueprint('board', __name__)


@main.route("/add_view")
def add_view():
    return render_template('board/add_view.html')


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    b = Board.new(**form)
    return redirect(url_for('index.index', board_id=b.id))
