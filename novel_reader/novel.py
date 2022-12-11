from flask import (
    Blueprint,
    render_template,
    request,
    session,
)
from novel_reader.db import get_db

bp = Blueprint("novel", __name__, url_prefix="/novel")


@bp.route("/<string:slug>/")
def novel_home(slug: str):
    chapters: list[dict] = []
    novel_id = slug
    data = get_novel(novel_id)[0]

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT genre_id FROM novel_genres WHERE novel_id = %s", (novel_id,))
    data["genres"] = [i["genre_id"] for i in cur.fetchall()]
    cur.execute("SELECT * FROM genre")
    genres = cur.fetchall()
    cur.execute("SELECT * FROM status")
    status = cur.fetchall()
    cur.execute("SELECT * FROM user WHERE id = %s", (data["user_id"],))
    author = cur.fetchone()
    cur.close()
    for i in get_chapters(novel_id):
        chapters.append(i)
    return render_template(
        "starter/novel.html",
        novel=data,
        chapters=chapters,
        first=get_first_chapter_id(novel_id),
        bookmark_check=bookmark_check,
        author=author,
        status=status,
        genres=genres,
    )


@bp.route("/<string:novel>/ch/<string:slug>/")
def chapter(novel: str, slug: str):
    chapter = get_chapter(slug)
    prev_chapter = get_prev_chapter_id(novel, chapter["id"])
    next_chapter = get_next_chapter_id(novel, chapter["id"])

    # Update view count of the novel by one when a chapter is loaded.
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE novel SET view = view + 1 WHERE id = %s;", (novel,))
    db.commit()
    cur.close()

    return render_template(
        "starter/chapter.html", chapter=chapter, prev=prev_chapter, next=next_chapter
    )


@bp.route("/latest/")
def latest():
    data: list = []
    for i in get_latest_novels(2147483647):
        data.append(i)

    return render_template("starter/list.html", endpoint="LATEST NOVELS", result=data)


@bp.route("/popular/")
def popular():
    data: list = []
    for i in get_most_viewed_novels(2147483647):
        data.append(i)

    return render_template("starter/list.html", endpoint="POPULAR NOVELS", result=data)


@bp.route("/status/<string:id>/")
def status(id: str):
    db = get_db()
    cur = cur = db.cursor(dictionary=True)
    cur.execute("SELECT name FROM status WHERE id = %s", (id,))
    status = cur.fetchone()
    cur.execute("SELECT * FROM novel where status_id = %s ORDER BY modified DESC", (id,))
    data = cur.fetchall()
    cur.close()
    return render_template(
        "starter/list.html", endpoint=f"{status['name'].upper()} NOVELS", result=data
    )


@bp.route("/author/<string:id>/")
def author(id: str):
    db = get_db()
    cur = cur = db.cursor(dictionary=True)
    cur.execute("SELECT username FROM user WHERE id = %s", (id,))
    author = cur.fetchone()
    cur.execute("SELECT * FROM novel where user_id = %s ORDER BY modified DESC", (id,))
    data = cur.fetchall()
    cur.close()
    return render_template(
        "starter/list.html",
        endpoint=f"{author['username'].upper()}'S NOVELS",
        result=data,
    )


@bp.route("/genre/<string:id>/")
def genre(id: str):
    db = get_db()
    cur = cur = db.cursor(dictionary=True)
    cur.execute("SELECT name FROM genre WHERE id = %s", (id,))
    genre = cur.fetchone()
    cur.execute(
        "SELECT * FROM novel WHERE id in (SELECT novel_id FROM novel_genres WHERE genre_id = %s) ORDER BY modified DESC;",
        (id,),
    )
    data = cur.fetchall()
    cur.close()
    return render_template(
        "starter/list.html", endpoint=f"{genre['name'].upper()} NOVELS", result=data
    )


@bp.route("/search/")
def search():
    text = request.args.get("q")
    db = get_db()
    cur = cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM novel WHERE name LIKE %s ORDER BY modified DESC;",
        (f"%{text}%",),
    )
    data = cur.fetchall()
    cur.close()
    return render_template(
        "starter/list.html", endpoint=f"SEARCH: {text.upper()}", result=data
    )


def get_chapters(novel_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM chapter WHERE novel_id = %s ORDER BY created DESC;", (novel_id,)
    )
    chapters = cur.fetchall()
    db.commit()
    cur.close()

    return chapters


def get_chapter(chapter_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM chapter WHERE id = %s;", (chapter_id,))
    chapter = cur.fetchall()
    db.commit()
    cur.close()

    return chapter[0]


def get_novel(novel_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM novel WHERE id = %s;", (novel_id,))
    novel = cur.fetchall()
    db.commit()
    cur.close()

    return novel


def get_first_chapter_id(novel_id):
    db = get_db()
    cur = db.cursor(buffered=True)
    cur.execute(
        "SELECT id FROM chapter WHERE novel_id = %s ORDER BY id ASC LIMIT 1",
        (novel_id,),
    )
    chapter_id = cur.fetchone()

    db.commit()
    cur.close()
    if chapter_id is None:
        return None

    return chapter_id[0]


def get_next_chapter_id(novel_id, current_chapter_num):
    db = get_db()
    cur = db.cursor(buffered=True)
    cur.execute(
        "SELECT id FROM chapter\
        WHERE novel_id = %s AND id > %s\
        ORDER BY id LIMIT 1;",
        (novel_id, current_chapter_num),
    )
    chapter_id = cur.fetchone()
    db.commit()
    cur.close()
    if chapter_id is None:
        return None

    return chapter_id[0]


def get_prev_chapter_id(novel_id, current_chapter_num):
    db = get_db()
    cur = db.cursor(buffered=True)
    cur.execute(
        "SELECT id FROM chapter\
        WHERE novel_id = %s AND id < %s\
        ORDER BY id LIMIT 1;",
        (novel_id, current_chapter_num),
    )
    chapter_id = cur.fetchone()
    db.commit()
    cur.close()
    if chapter_id is None:
        return None

    return chapter_id[0]


def get_latest_novels(n=10):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM novel ORDER BY modified DESC LIMIT %s;", (n,))
    novels = cur.fetchall()
    db.commit()
    cur.close()
    return novels


def get_most_viewed_novels(n=10):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM novel ORDER BY view DESC LIMIT %s;", (n,))
    novels = cur.fetchall()
    db.commit()
    cur.close()
    return novels


def bookmark_check(novel_id):  # Return False if there is bookmark, True if no bookmark
    db = get_db()
    cur = db.cursor(buffered=True)

    cur.execute(
        "SELECT * FROM bookmark WHERE user_id = %s AND novel_id = %s;",
        (session["user_id"], novel_id),
    )
    result = cur.fetchone()
    if result is None:
        db.commit()
        cur.close()
        return True
    db.commit()
    cur.close()
    return False
