from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from novel_reader.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route("/")
def home():
    # This is sample data for showing template
    popular: list[dict[str, str]] = []
    latest: list = []
    for _ in range(18):
        popular.append(
            {
                "name": "Novel Name",
                "image": "/static/cover-default.png",
                "get_absolute_url": "/novel-slug/",
                "alt": "alt",
                "latest_chap": "chapter X",
            }
        )

    for _ in range(30):
        latest.append({
            "name": "Best Novel",
            "image": "/static/cover-default.png",
            "get_absolute_url": "/novel/novel-slug/",
            "alt": "alt",
            "chapters": [
                {"name": "chapter XX", "get_absolute_url": "/chapter/slug/", "get_date": "2 hours ago"}, 
                {"name": "chapter XX", "get_absolute_url": "/chapter/slug/", "get_date": "2 hours ago"}
                ]
            })
    return render_template("starter/home.html", popular=popular, latest=latest)

@bp.route("/latest/")
def latest():
    pass


@bp.route("/popular/")
def popular():
    pass


@bp.route("/status/on_going/")
def on_going():
    pass


@bp.route("/status/complete/")
def completed():
    pass


@bp.route("/status/hiatus/")
def hiatus():
    pass