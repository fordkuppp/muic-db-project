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
from novel_reader.user import bookmark_check
from typing import Any

bp = Blueprint("novel", __name__, url_prefix="/novel")

@bp.route("/<string:slug>/")
def novel_home(slug: str):
    chapters: list[dict] = []
    novel_id = slug
    
    for i in get_chapters(novel_id):
        chapters.append(i)
        
    data = get_novel(novel_id)
    return render_template("starter/novel.html", novel=data[0], chapters = chapters, first=get_first_chapter_id(novel_id), bookmark_check=bookmark_check)

@bp.route("/<string:novel>/ch/<string:slug>/")
def chapter(novel: str, slug: str):
    chapter = get_chapter(slug)
    prev_chapter = get_prev_chapter_id(novel, chapter["chapter_num"])
    next_chapter = get_next_chapter_id(novel, chapter["chapter_num"])
    
    # Update view count of the novel by one when a chapter is loaded.
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE novel SET view = view + 1 WHERE id = %s;",
        (novel,)
    )
    db.commit()
    cur.close()
    
    return render_template("starter/chapter.html", chapter=chapter, prev=prev_chapter, next=next_chapter)

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

def get_chapters(novel_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM chapter WHERE novel_id = %s;",
        (novel_id,)
    )
    chapters = cur.fetchall()
    db.commit()
    cur.close()
    
    return chapters

def get_chapter(chapter_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM chapter WHERE id = %s;",
        (chapter_id,)
    )
    chapter = cur.fetchall()
    db.commit()
    cur.close()
    
    return chapter[0]

def get_novel(novel_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM novel WHERE id = %s;",
        (novel_id,)
    )
    novel = cur.fetchall()
    db.commit()
    cur.close()
    
    return novel

def get_first_chapter_id(novel_id):
    db = get_db()
    cur = db.cursor(buffered=True)
    cur.execute(
        "SELECT chapter_num FROM chapter WHERE novel_id = %s ORDER BY id LIMIT 1;",
        (novel_id,)
    )
    chapter_num = cur.fetchone()

    if chapter_num is None:
        db.commit()
        cur.close()
        return None
    
    cur.execute(
        "SELECT id FROM chapter WHERE novel_id = %s AND chapter_num = %s;",
        (novel_id, chapter_num[0],)
    )
    chapter_id = cur.fetchone()
    
    db.commit()
    cur.close()

    return chapter_id[0]

def get_next_chapter_id(novel_id, current_chapter_num):
    db = get_db()
    cur = db.cursor(buffered=True)
    cur.execute(
        "SELECT chapter_num FROM chapter\
        WHERE novel_id = %s AND chapter_num > %s\
        ORDER BY id LIMIT 1;",
        (novel_id, current_chapter_num)
    )
    next_chapter_num = cur.fetchone()

    if next_chapter_num is None:
        db.commit()
        cur.close()
        return None
    
    cur.execute(
        "SELECT id FROM chapter WHERE novel_id = %s AND chapter_num = %s;",
        (novel_id, next_chapter_num[0],)
    )
    chapter_id = cur.fetchone()
    
    db.commit()
    cur.close()

    return chapter_id[0]

def get_prev_chapter_id(novel_id, current_chapter_num):
    db = get_db()
    cur = db.cursor(buffered=True)
    cur.execute(
        "SELECT chapter_num FROM chapter\
        WHERE novel_id = %s AND chapter_num < %s\
        ORDER BY id LIMIT 1;",
        (novel_id, current_chapter_num)
    )
    prev_chapter_num = cur.fetchone()
    
    if prev_chapter_num is None:
        db.commit()
        cur.close()
        return None
    
    cur.execute(
        "SELECT id FROM chapter WHERE novel_id = %s AND chapter_num = %s;",
        (novel_id, prev_chapter_num[0],)
    )
    chapter_id = cur.fetchone()
    
    db.commit()
    cur.close()

    return chapter_id[0]

def get_latest_novels(n=10):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM novel ORDER BY modified LIMIT %s;",
        (n,)
    )
    novels = cur.fetchall()
    db.commit()
    cur.close()
    
    return novels

def get_most_viewed_novels(n=10):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM novel ORDER BY view LIMIT %s;",
        (n,)
    )
    novels = cur.fetchall()
    db.commit()
    cur.close()
    
    return novels