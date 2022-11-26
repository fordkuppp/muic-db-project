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
    print(novels)
    return render_template("starter/admin.html", novels = novels)

@bp.route("/novel/edit")
def novel_edit():
    return "pretend this works"

@bp.route("/novel/add", methods=["POST"])
def novel_add():
    return "pretend this works"