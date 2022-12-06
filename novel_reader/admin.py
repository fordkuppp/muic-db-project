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
    role_id = session.get('role_id')
    if role_id != 2:
        return "You are not an admin!"
        
@bp.route("/")
def admin():   
    db = get_db()
    cur = db.cursor(dictionary=True)  
    cur.execute("SELECT * FROM novel")
    novels = cur.fetchall()
    cur.close()
    return render_template("starter/admin/admin.html", novels = novels)

@bp.route("/novel/edit")
def novel_edit():
    db = get_db()
    cur = db.cursor(dictionary=True)  
    novel_id = request.args.get("novelId")
    cur.execute("SELECT * FROM chapter WHERE novel_id = %s", (novel_id,))
    chapters = cur.fetchall()
    cur.close()
    return render_template("starter/admin/novel/edit.html", chapters = chapters, novel_id = novel_id)

@bp.route("/chapter/edit", methods=["POST"])
def chapter_edit():
    chapter_name = request.form["chapterName"]
    chapter_content = request.form["chapterContent"]
    chapter_id = request.form["chapterId"]
    novel_id = request.form["novelId"]
    print(chapter_name, chapter_id)
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    cur.execute(
        "UPDATE chapter SET name = %s WHERE id = %s;",
        (chapter_name, chapter_id)
    )
    cur.execute(
        "UPDATE chapter SET content = %s WHERE id = %s;",
        (chapter_content, chapter_id)
    )
    cur.execute("SELECT * FROM chapter WHERE novel_id = %s", (novel_id,))
    chapters = cur.fetchall()
    db.commit()
    cur.close()
        
    return render_template("starter/admin/novel/edit.html", chapters = chapters, novel_id = novel_id)

@bp.route("/chapter/add", methods=["POST"])
def chapter_add():
    chapter_name = request.form["chapterName"]
    chapter_content = request.form["chapterContent"]
    novel_id = request.form["novelId"]
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    cur.execute(
        "INSERT INTO reader_db.chapter (name, novel_id, content)\
        VALUES (%s, %s, %s);",
        (chapter_name, novel_id, chapter_content)
    )

    cur.execute("SELECT * FROM chapter WHERE novel_id = %s", (novel_id,))
    chapters = cur.fetchall()
    db.commit()
    cur.close()
        
    return render_template("starter/admin/novel/edit.html", chapters = chapters, novel_id = novel_id)

@bp.route("/add", methods=["POST"])
def novel_add():
    novel_name = request.form["novelName"]
    novel_image = request.form["novelImage"]
    novel_description = request.form["novelDescription"]
    novel_genre = "Action"
    now = datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "INSERT INTO reader_db.novel (name, image, description, created, modified, genre_name, status_id)\
        VALUES (%s, %s, %s, %s, %s, %s, 1);", # TODO make the genre/status id chooseable from dropdown box
        (novel_name, novel_image, novel_description, now, now, novel_genre)
    )
    db.commit()
    cur.close()
    
    return redirect("/")

@bp.route("/remove", methods=["GET","DELETE"])
def novel_remove():
    novel_id = request.args.get("novel-id")
    
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "DELETE FROM reader_db.chapter WHERE novel_id = %s;",
        (novel_id,)
    )
    db.commit()
    cur.execute(
        "DELETE FROM reader_db.novel WHERE id = %s;",
        (novel_id,)
    )
    db.commit()
    cur.close()
    
    return redirect("/")