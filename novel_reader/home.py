from mysql.connector.errors import InternalError
from flask import (
    Blueprint,
    render_template,
)
from novel_reader.novel import get_most_viewed_novels, get_latest_novels
from novel_reader.db import get_db

bp = Blueprint("home", __name__, url_prefix="/")


@bp.route("/")
def home():
    popular: list[dict[str, str]] = []
    latest: list = []
    db = get_db()
    cur = db.cursor(dictionary=True, buffered=True)
    for i in get_most_viewed_novels(18):
        temp: dict = i.copy()
        try:
            cur.execute(
                f"SELECT name FROM chapter WHERE novel_id = {temp['id']} ORDER BY created DESC;"
            )
            temp["latest_chap"] = cur.fetchone().get("name")
        except AttributeError:
            pass
        finally:
            popular.append(temp)
    for i in get_latest_novels(28):
        temp: dict = i.copy()
        try:
            cur.execute(
                f"SELECT id, name, created FROM chapter WHERE novel_id = {temp['id']} ORDER BY created DESC;"
            )
            temp["chapters"] = cur.fetchmany(2)
        except AttributeError:
            pass
        finally:
            latest.append(temp)
    cur.close()
    return render_template("starter/home.html", popular=popular, latest=latest)
