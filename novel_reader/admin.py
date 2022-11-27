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

@bp.route("/edit")
def novel_edit():
    db = get_db()
    cur = db.cursor(dictionary=True)  
    novel_id = request.args.get('id')
    cur.execute("SELECT * FROM chapter WHERE novel_id = %s", (novel_id,))
    chapters = cur.fetchall()
    cur.close()
    return render_template("starter/admin/novel/edit.html", chapters = chapters)

@bp.route("/edit", methods=["POST"])
def chapter_edit():
    chapter_name = request.form["chapterName"]
    chapter_content = request.form["chapterContent"]
    chapter_id = request.args.get('id')
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
    db.commit()
    cur.close()
        
    return novel_edit()

@bp.route("/add", methods=["POST"])
def novel_add():
    return "pretend this works"