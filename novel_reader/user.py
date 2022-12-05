from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from novel_reader.db import get_db
from datetime import datetime
from mysql.connector import IntegrityError
import bcrypt

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/profile")
def profile():
    user_id = session.get("user_id")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM bookmark WHERE user_id = %s", (user_id,))
    novel_id = cur.fetchall()
    bookmarks = []
    for novel_id in novel_id:
        cur.execute("SELECT * FROM novel WHERE id = %s", (novel_id["novel_id"],))
        bookmarks.append(cur.fetchall())

    cur.close()
    return render_template("starter/user/profile.html", bookmarks=bookmarks)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        g.user = cur.fetchone()
        cur.close()


@bp.route("/register", methods=["POST"])
def register():
    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        next = request.args.get("next")
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        email = request.form["email"]
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password1.encode("utf-8"), salt)

        if password1 != password2:
            session["signup_pass"] = "Password don not match!"
            return redirect(next)

        add_user = (
            "INSERT INTO reader_db.user "
            "(username, email, password, last_login, role_id) "
            "VALUES (%s, %s, %s, %s, 1);"
        )
        data_user = (username, email, hashed_password, time)

        cur.execute(add_user, data_user)
        db.commit()

        cur.execute("SELECT * FROM user WHERE username = %s;", (username,))

        user = cur.fetchone()

        session.clear()
        cur.close()
        session["user_id"] = user["id"]
        session["role_id"] = user["role_id"]

        return redirect(next)

    except IntegrityError:
        session["signup_user"] = "Username or email is already in used!"
        return redirect(next)


@bp.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    next = request.args.get("next")
    print(next)

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cur.fetchone()

    if (user is None) or (
        not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8"))
    ):
        session["login_error"] = "Invalid username or password"
        return redirect(next)

    cur.close()
    session.clear()
    session["user_id"] = user["id"]
    session["role_id"] = user["role_id"]
    return redirect(next)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@bp.route("/forget", methods=["POST"])
def forget():
    pass


@bp.route("/forget/<string:token>/", methods=["POST", "GET"])
def new_pass(token: str):
    if request.method == "POST":
        pass
    else:
        return render_template("starter/reset.html")


@bp.route("/novels")
def novels():
    latest: list = []
    for _ in range(30):
        latest.append(
            {
                "name": "Best Novel",
                "image": "/static/cover-default.png",
                "slug": "best-novel",
                "alt": "alt",
                "chapters": [
                    {
                        "name": "chapter XX",
                        "slug": "chapter-xx",
                        "get_date": "2 hours ago",
                    },
                    {
                        "name": "chapter XX",
                        "slug": "chapter-xx",
                        "get_date": "2 hours ago",
                    },
                ],
            }
        )
    return render_template("starter/user/novel.html", latest=latest)


@bp.route("/bookmarks")
def bookmarks():
    latest: list = []
    for _ in range(28):
        latest.append(
            {
                "name": "Best Novel",
                "image": "/static/cover-default.png",
                "slug": "best-novel",
                "alt": "alt",
                "chapters": [
                    {
                        "name": "chapter XX",
                        "slug": "chapter-xx",
                        "get_date": "2 hours ago",
                    },
                    {
                        "name": "chapter XX",
                        "slug": "chapter-xx",
                        "get_date": "2 hours ago",
                    },
                ],
            }
        )
    return render_template("starter/user/bookmarks.html", latest=latest)
