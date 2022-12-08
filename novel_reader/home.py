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
from typing import Any
from novel_reader.novel import get_most_viewed_novels, get_latest_novels

bp = Blueprint("home", __name__, url_prefix="/")


@bp.route("/")
def home():
    popular: list[dict[str, str]] = []
    latest: list = []
    for i in get_most_viewed_novels(18):
        popular.append(i)
    for i in get_latest_novels(28):
        latest.append(i)

    return render_template("starter/home.html", popular=popular, latest=latest)


@bp.route("/status/active/")
def on_going():
    data: list[dict] = []
    for _ in range(40):
        data.append(
            {
                "name": "Best Novel",
                "image": "/static/cover-default.png",
                "slug": "best-novel",
                "alt": "alt",
                "hits": 30,
                "description": "This is novel description that is very very and very super duper long.",
                "genres": [
                    {"name": "Action", "slug": "action"},
                    {"name": "Martial Arts", "slug": "martial-arts"},
                ],
                "latest_chap": "chapter XX",
            }
        )

    return render_template("starter/list.html", endpoint="ON-GOING NOVELS", result=data)


@bp.route("/status/complete/")
def completed():
    data: list[dict] = []
    for _ in range(40):
        data.append(
            {
                "name": "Best Novel",
                "image": "/static/cover-default.png",
                "slug": "best-novel",
                "alt": "alt",
                "hits": 30,
                "description": "This is novel description that is very very and very super duper long.",
                "genres": [
                    {"name": "Action", "slug": "action"},
                    {"name": "Martial Arts", "slug": "martial-arts"},
                ],
                "latest_chap": "chapter XX",
            }
        )

    return render_template("starter/list.html", endpoint="COMPLETED NOVELS", result=data)


@bp.route("/status/hiatus/")
def hiatus():
    data: list[dict] = []
    for _ in range(40):
        data.append(
            {
                "name": "Best Novel",
                "image": "/static/cover-default.png",
                "slug": "best-novel",
                "alt": "alt",
                "hits": 30,
                "description": "This is novel description that is very very and very super duper long.",
                "genres": [
                    {"name": "Action", "slug": "action"},
                    {"name": "Martial Arts", "slug": "martial-arts"},
                ],
                "latest_chap": "chapter XX",
            }
        )
    return render_template("starter/list.html", endpoint="HIATUS NOVELS", result=data)


@bp.route("/search/")
def search():
    data: list[dict] = []
    for _ in range(40):
        data.append(
            {
                "name": "Best Novel",
                "image": "/static/cover-default.png",
                "slug": "best-novel",
                "alt": "alt",
                "hits": 30,
                "description": "This is novel description that is very very and very super duper long.",
                "genres": [
                    {"name": "Action", "slug": "action"},
                    {"name": "Martial Arts", "slug": "martial-arts"},
                ],
                "latest_chap": "chapter XX",
            }
        )
    return render_template("starter/list.html", endpoint="SEARCH: KEYWORD", result=data)
