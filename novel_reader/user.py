from flask import (
    Blueprint,
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
from novel_reader.novel import get_chapters, get_novel
import bcrypt

bp = Blueprint("user", __name__, url_prefix="/user")


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


@bp.route("/register", methods=["POST"])
def register():
    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        next_path = request.args.get("next")
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        email = request.form["email"]
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password1.encode("utf-8"), salt)

        if password1 != password2:
            session["signup_pass"] = "Password don not match!"
            return redirect(next_path)

        add_user = (
            "INSERT INTO user "
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

        return redirect(next_path)

    except IntegrityError:
        session["signup_user"] = "Username or email is already in used!"
        return redirect(next_path)


@bp.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    next_path = request.args.get("next")

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cur.fetchone()

    if (user is None) or (
        not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8"))
    ):
        session["login_error"] = "Invalid username or password"
        return redirect(next_path)

    cur.close()
    session.clear()
    session["user_id"] = user["id"]
    session["role_id"] = user["role_id"]
    return redirect(next_path)


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


@bp.route("/bookmark/add/<string:novel_id>/", methods=["POST"])
def bookmark_add(novel_id: str):
    user_id = session["user_id"]

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "INSERT INTO bookmark (user_id, novel_id) VALUES (%s, %s);",
        (user_id, novel_id),
    )
    db.commit()
    cur.close()

    return redirect("/novel/" + novel_id)


@bp.route("/bookmark/remove/<string:novel_id>/", methods=["POST"])
def bookmark_remove(novel_id: str):
    user_id = session["user_id"]

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "DELETE FROM bookmark WHERE user_id = %s AND novel_id = %s;", (user_id, novel_id)
    )
    db.commit()
    cur.close()

    return redirect("/novel/" + novel_id)


@bp.route("/bookmarks")
def bookmarks():
    user_id = session["user_id"]

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT novel_id FROM bookmark WHERE user_id = %s;", (user_id,))
    bookmarks_list = cur.fetchall()

    novels: list = []
    for i in bookmarks_list:
        cur.execute("SELECT * FROM novel WHERE id = %s;", (i["novel_id"],))
        novels.append(cur.fetchone())

    db.commit()
    cur.close()
    return render_template("starter/user/bookmarks.html", novels=novels)


@bp.route("/novels/")
def your_novel():
    user_id = session["user_id"]
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM novel WHERE user_id = %s ORDER BY modified DESC", (user_id,)
    )
    novels = cur.fetchall()
    cur.execute("SELECT * FROM genre ORDER BY name")
    genres = cur.fetchall()
    cur.execute("SELECT * FROM status")
    status = cur.fetchall()
    cur.close()
    return render_template(
        "starter/user/novel.html", novels=novels, genres=genres, status=status
    )


@bp.route("/novel/add/", methods=["POST"])
def novel_add():
    novel_name = request.form["name"]
    novel_image = request.form["image"]
    novel_description = request.form["description"]
    novel_author = session["user_id"]
    novel_status = request.form["status"]
    novel_genres = request.form.getlist("genres")
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "INSERT INTO novel (name, image, description, created, modified, user_id, status_id)\
        VALUES (%s, %s, %s, %s, %s, %s, %s);",  # TODO make the genre/status id chooseable from dropdown box
        (
            novel_name,
            novel_image,
            novel_description,
            now,
            now,
            novel_author,
            novel_status,
        ),
    )
    db.commit()
    cur.execute("SELECT * FROM novel where created = %s;", (now,))
    novel = cur.fetchone()
    for i in novel_genres:
        cur.execute(
            "INSERT INTO novel_genres (novel_id, genre_id) VALUES (%s, %s);",
            (novel["id"], i),
        )
    db.commit()
    cur.close()
    return redirect(url_for("user.your_novel"))


@bp.route("/novel/edit/", methods=["POST"])
def novel_edit():
    novel = get_novel(request.form["novel_id"])[0]
    if novel["user_id"] != session["user_id"]:
        return redirect(url_for("user.your_novel"))
    novel_name = request.form["name"]
    novel_image = request.form["image"]
    novel_description = request.form["description"]
    novel_status = request.form["status"]
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "UPDATE novel SET name=%s, image=%s, description=%s, status_id=%s WHERE id=%s;",
        (novel_name, novel_image, novel_description, novel_status, novel["id"]),
    )
    db.commit()
    cur.close()
    return redirect(url_for("user.your_novel"))


@bp.route("/novel/remove/", methods=["GET"])
def novel_remove():
    novel = get_novel(request.args.get("novelId"))[0]
    if novel["user_id"] != session["user_id"]:
        return redirect(url_for("user.your_novel"))
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("DELETE FROM novel WHERE id = %s;", (novel["id"],))
    db.commit()
    cur.close()
    return redirect(url_for("user.your_novel"))


@bp.route("/chapter/")
def chapter():
    db = get_db()
    cur = db.cursor(dictionary=True)
    novel = get_novel(request.args.get("novelId"))[0]
    if novel["user_id"] != session["user_id"]:
        return redirect(url_for("user.your_novel"))
    chapters = get_chapters(novel["id"])
    cur.close()
    return render_template("starter/user/chapter.html", chapters=chapters, novel=novel)


@bp.route("/chapter/edit/", methods=["POST"])
def chapter_edit():
    chapter_name = request.form["chapterName"]
    chapter_content = request.form["chapterContent"]
    chapter_id = request.form["chapterId"]
    novel = get_novel(request.form["novelId"])[0]
    if novel["user_id"] != session["user_id"]:
        return redirect(url_for("user.your_novel"))
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "UPDATE chapter SET name = %s, content = %s WHERE id = %s;",
        (chapter_name, chapter_content, chapter_id),
    )
    db.commit()
    cur.close()

    return redirect(url_for("user.chapter") + f"?novelId={novel['id']}")


@bp.route("/chapter/add/", methods=["POST"])
def chapter_add():
    chapter_name = request.form["chapterName"]
    chapter_content = request.form["chapterContent"]
    novel = get_novel(request.form["novelId"])[0]
    if novel["user_id"] != session["user_id"]:
        return redirect(url_for("user.your_novel"))
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "INSERT INTO chapter (name, novel_id, content, created)\
        VALUES (%s, %s, %s, %s);",
        (chapter_name, novel["id"], chapter_content, now),
    )
    cur.execute("UPDATE novel SET modified = %s WHERE id = %s;", (now, novel["id"]))

    db.commit()
    cur.close()

    return redirect(url_for("user.chapter") + f"?novelId={novel['id']}")


@bp.route("/chapter/remove/", methods=["GET", "DELETE"])
def chapter_remove():
    chapter_id = request.args.get("chapterId")
    novel = get_novel(request.args.get("novelId"))[0]
    if novel["user_id"] != session["user_id"]:
        return redirect(url_for("user.your_novel"))
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("DELETE FROM reader_db.chapter WHERE id = %s;", (chapter_id,))

    db.commit()
    cur.close()

    return redirect(url_for("user.chapter") + f"?novelId={novel['id']}")
