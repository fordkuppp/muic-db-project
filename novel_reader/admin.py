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
from novel_reader.novel import get_chapters, get_novel

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.before_request
def check_admin_role():
    role_id = session.get("role_id")
    if role_id != 2:
        return redirect("/")


@bp.route("/novel/")
def novel():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM novel ORDER BY modified DESC")
    novels = cur.fetchall()
    cur.close()
    return render_template(
        "starter/admin/admin.html",
        novels=novels,
        page="admin",
    )


@bp.route("/novel/remove/", methods=["GET"])
def novel_remove():
    novel_id = request.args.get("novelId")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("DELETE FROM chapter WHERE novel_id = %s;", (novel_id,))
    db.commit()
    cur.execute("DELETE FROM novel WHERE id = %s;", (novel_id,))
    db.commit()
    cur.execute("DELETE FROM bookmark WHERE novel_id = %s;", (novel_id,))
    db.commit()
    cur.close()
    return redirect(url_for("admin.novel"))


@bp.route("/chapter/")
def chapter():
    db = get_db()
    cur = db.cursor(dictionary=True)
    novel = get_novel(request.args.get("novelId"))[0]
    chapters = get_chapters(novel["id"])
    cur.close()
    return render_template("starter/admin/chapter.html", chapters=chapters, novel=novel)


@bp.route("/chapter/remove/", methods=["GET", "DELETE"])
def chapter_remove():
    chapter_id = request.args.get("chapterId")
    novel_id = request.args.get("novelId")

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("DELETE FROM reader_db.chapter WHERE id = %s;", (chapter_id,))

    db.commit()
    cur.close()

    return redirect(url_for("admin.chapter") + f"?novelId={novel_id}")


@bp.route("/user/")
def user():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM user")
    users = cur.fetchall()
    cur.close()
    return render_template("starter/admin/user.html", users=users)


@bp.route("/user/add", methods=["POST"])
def add_user():
    db = get_db()
    cur = db.cursor(dictionary=True)
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    email = request.form["email"]
    role = request.form.get("role")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password1.encode("utf-8"), salt)

    add_user = (
        "INSERT INTO user "
        "(username, email, password, last_login, role_id) "
        "VALUES (%s, %s, %s, %s, %s);"
    )
    data_user = (username, email, hashed_password, time, role)

    cur.execute(add_user, data_user)
    db.commit()

    return redirect(url_for("admin.user"))


@bp.route("/user/remove", methods=["GET"])
def user_remove():
    user_id = request.args.get("userId")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("DELETE FROM bookmark WHERE user_id = %s;", (user_id,))
    db.commit()
    cur.execute("DELETE FROM user WHERE id = %s;", (user_id,))
    db.commit()
    cur.close()

    return redirect(url_for("admin.user"))


@bp.route("/user/edit/email", methods=["POST"])
def user_edit_email():
    user_id = request.args.get("userId")
    email = request.form["email"]

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("UPDATE user SET email = %s WHERE id = %s;", (email, user_id))
    db.commit()
    cur.close()

    return redirect(url_for("admin.user"))


@bp.route("/user/edit/role", methods=["POST"])
def user_edit_role():
    user_id = request.args.get("userId")
    role = request.form.get("role")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("UPDATE user SET role_id = %s WHERE id = %s;", (role, user_id))
    db.commit()
    cur.close()

    return redirect(url_for("admin.user"))


@bp.route("/genre/")
def genre():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM genre ORDER BY name")
    genres = cur.fetchall()
    cur.close()
    return render_template("starter/admin/genre.html", genres=genres)


@bp.route("/genre/edit/", methods=["POST"])
def genre_edit():
    name = request.form["name"]
    id = request.form["id"]
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("UPDATE genre SET name = %s WHERE id = %s;", (name, id))
    db.commit()
    cur.close()

    return redirect(url_for("admin.genre"))


@bp.route("/genre/add/", methods=["POST"])
def genre_add():
    name = request.form["name"]
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("INSERT INTO genre (name) VALUES (%s);", (name,))
    db.commit()
    cur.close()

    return redirect(url_for("admin.genre"))


@bp.route("/genre/remove/", methods=["GET", "DELETE"])
def genre_remove():
    id = request.args.get("id")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("DELETE FROM novel_genres where genre_id = %s;", (id,))
    cur.execute("DELETE FROM genre WHERE id = %s;", (id,))
    db.commit()
    cur.close()

    return redirect(url_for("admin.genre"))


@bp.route("/status/")
def status():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM status ORDER BY name")
    status = cur.fetchall()
    cur.close()
    return render_template("starter/admin/status.html", status=status)


@bp.route("/status/edit/", methods=["POST"])
def status_edit():
    name = request.form["name"]
    id = request.form["id"]
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("UPDATE status SET name = %s WHERE id = %s;", (name, id))
    db.commit()
    cur.close()

    return redirect(url_for("admin.status"))


@bp.route("/status/add/", methods=["POST"])
def status_add():
    name = request.form["name"]
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("INSERT INTO status (name) VALUES (%s);", (name,))
    db.commit()
    cur.close()

    return redirect(url_for("admin.status"))


@bp.route("/status/remove/", methods=["GET", "DELETE"])
def status_remove():
    id = request.args.get("id")
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("DELETE FROM status WHERE id = %s;", (id,))
    db.commit()
    cur.close()

    return redirect(url_for("admin.status"))
