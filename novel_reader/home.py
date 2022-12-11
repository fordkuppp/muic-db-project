from flask import (
    Blueprint,
    render_template,
)
from novel_reader.novel import get_most_viewed_novels, get_latest_novels

bp = Blueprint("home", __name__, url_prefix="/")


@bp.route("/")
def home():
    popular: list[dict[str, str]] = []
    latest: list = []
    for i in get_most_viewed_novels(18):
        popular.append(i)
    for i in get_latest_novels(28):
        latest.append(i)

    return render_template("starter/home.html", popular=popular, latest=latest)
