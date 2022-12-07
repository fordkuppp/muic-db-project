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

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.before_request
def check_admin_role():
    role_id = session.get("role_id")
    if role_id != 2:
        return "You are not an admin!"


@bp.route("/")
def admin():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM novel")
    novels = cur.fetchall()
    cur.close()
    return render_template("starter/admin/admin.html", novels=novels)


@bp.route("/novel/edit")
def novel_edit():
    db = get_db()
    cur = db.cursor(dictionary=True)
    novel_id = request.args.get("novelId")
    cur.execute("SELECT * FROM chapter WHERE novel_id = %s", (novel_id,))
    chapters = cur.fetchall()
    cur.close()
    return render_template(
        "starter/admin/chapter.html", chapters=chapters, novel_id=novel_id
    )


@bp.route("/user/edit")
def user_edit():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM user")
    users = cur.fetchall()
    cur.close()
    return render_template("starter/admin/user.html", users=users)


@bp.route("/chapter/edit", methods=["POST"])
def chapter_edit():
    chapter_name = request.form["chapterName"]
    chapter_content = request.form["chapterContent"]
    chapter_num = request.form["chapterNum"]
    chapter_id = request.form["chapterId"]
    novel_id = request.form["novelId"]
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("UPDATE chapter SET name = %s WHERE id = %s;", (chapter_name, chapter_id))
    cur.execute(
        "UPDATE chapter SET content = %s WHERE id = %s;", (chapter_content, chapter_id)
    )
    cur.execute(
        "UPDATE chapter SET chapter_num = %s WHERE id = %s;", (chapter_num, chapter_id)
    )
    # cur.execute("SELECT * FROM chapter WHERE novel_id = %s", (novel_id,))
    # chapters = cur.fetchall()

    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("UPDATE novel SET modified = %s WHERE id = %s;", (now, novel_id))

    db.commit()
    cur.close()

    return redirect(url_for("admin.novel_edit") + f"?novelId={novel_id}")


@bp.route("/chapter/add", methods=["POST"])
def chapter_add():
    chapter_name = request.form["chapterName"]
    chapter_content = request.form["chapterContent"]
    chapter_num = request.form["chapterNum"]
    novel_id = request.form["novelId"]
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "INSERT INTO reader_db.chapter (name, novel_id, content, chapter_num)\
        VALUES (%s, %s, %s, %s);",
        (chapter_name, novel_id, chapter_content, chapter_num),
    )

    # cur.execute("SELECT * FROM chapter WHERE novel_id = %s", (novel_id,))
    # chapters = cur.fetchall()

    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("UPDATE novel SET modified = %s WHERE id = %s;", (now, novel_id))

    db.commit()
    cur.close()

    return redirect(url_for("admin.novel_edit") + f"?novelId={novel_id}")


@bp.route("/chapter/remove", methods=["GET", "DELETE"])
def chapter_remove():
    chapter_id = request.args.get("chapterId")
    novel_id = request.args.get("novelId")

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("DELETE FROM reader_db.chapter WHERE id = %s;", (chapter_id,))

    db.commit()
    cur.close()

    return redirect(url_for("admin.novel_edit") + f"?novelId={novel_id}")


@bp.route("/add", methods=["POST"])
def novel_add():
    novel_name = request.form["novelName"]
    novel_image = request.form["novelImage"]
    novel_description = request.form["novelDescription"]
    novel_genre = "Action"
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "INSERT INTO reader_db.novel (name, image, description, created, modified, genre_name, status)\
        VALUES (%s, %s, %s, %s, %s, %s, 'Active');",  # TODO make the genre/status id chooseable from dropdown box
        (novel_name, novel_image, novel_description, now, now, novel_genre),
    )
    db.commit()
    cur.close()
    return redirect(url_for("admin.admin"))


@bp.route("/remove", methods=["GET"])
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

    return redirect(url_for("admin.admin"))


@bp.route("/rename", methods=["POST", "GET"])
def novel_edit_name():
    novel_id = request.args.get("novelId")
    name = request.form["novelName"]
    print(novel_id, name)
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("UPDATE novel SET name = %s WHERE id = %s;", (name, novel_id))
    db.commit()
    cur.close()

    return redirect(url_for("admin.admin"))


@bp.route("/edit/image", methods=["POST"])
def novel_edit_image():
    novel_id = request.args.get("novelId")
    image = request.form["novelImage"]

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("UPDATE novel SET image = %s WHERE id = %s;", (image, novel_id))
    db.commit()
    cur.close()

    return redirect(url_for("admin.admin"))


@bp.route("/edit/description", methods=["POST"])
def novel_edit_description():
    novel_id = request.args.get("novelId")
    description = request.form["novelDescription"]

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "UPDATE novel SET description = %s WHERE id = %s;", (description, novel_id)
    )
    db.commit()
    cur.close()

    return redirect(url_for("admin.admin"))


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
        "INSERT INTO reader_db.user "
        "(username, email, password, last_login, role_id) "
        "VALUES (%s, %s, %s, %s, %s);"
    )
    data_user = (username, email, hashed_password, time, role)

    cur.execute(add_user, data_user)
    db.commit()

    return redirect(url_for("admin.admin"))


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

    return redirect(url_for("admin.admin"))


@bp.route("/user/editEmail", methods=["POST"])
def user_edit_email():
    user_id = request.args.get("userId")
    email = request.form["email"]

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("UPDATE user SET email = %s WHERE id = %s;", (email, user_id))
    db.commit()
    cur.close()

    return redirect(url_for("admin.admin"))


@bp.route("/user/editRole", methods=["POST"])
def user_edit_role():
    user_id = request.args.get("userId")
    role = request.form.get("role")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("UPDATE user SET role_id = %s WHERE id = %s;", (role, user_id))
    db.commit()
    cur.close()

    return redirect(url_for("admin.admin"))
