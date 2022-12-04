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

bp = Blueprint("home", __name__, url_prefix="/")


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
                "slug": "best-novel",
                "alt": "alt",
                "latest_chap": "chapter X",
            }
        )

    for _ in range(30):
        latest.append(
            {
                "name": "Best Novel",
                "image": "/static/cover-default.png",
                "slug": "best-novel",
                "alt": "alt",
                "chapters": [
                    {
                        "name": "chapter XX",
                        "slug": "chapter-xx",
                        "get_date": "2 hours ago",
                    },
                    {
                        "name": "chapter XX",
                        "slug": "chapter-xx",
                        "get_date": "2 hours ago",
                    },
                ],
            }
        )
    return render_template("starter/home.html", popular=popular, latest=latest)


@bp.route("/latest/")
def latest():
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

    return render_template("starter/list.html", endpoint="LATEST NOVELS", result=data)


@bp.route("/popular/")
def popular():
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

    return render_template("starter/list.html", endpoint="POPULAR NOVELS", result=data)


@bp.route("/status/on_going/")
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


@bp.route("/<string:slug>/")
def novel(slug: str):
    chapters: list[dict] = []
    for i in range(20):
        chapters.append(
            {"name": f"chapter {i}", "slug": f"chapter-{i}", "created": "1 day ago"}
        )
    data: dict = {
        "name": "Best Novel",
        "image": "/static/cover-default.png",
        "slug": "best-novel",
        "alt": "alt",
        "hits": 30,
        "description": "This is novel description that is very very and very super duper long.",
        "author": {"username": "user 007", "slug": "user-007"},
        "status": {"name": "On going", "slug": "on-going"},
        "genres": [
            {"name": "Action", "slug": "action"},
            {"name": "Martial Arts", "slug": "martial-arts"},
        ],
        "chapters": chapters,
        "modified": "1 day ago",
    }
    return render_template("starter/novel.html", novel=data)


@bp.route("/<string:novel>/ch/<string:slug>/")
def chapter(novel: str, slug: str):
    chapter: dict = {
        "name": "CHAPTER 01",
        "slug": "chapter-01",
        "novel": {"name": "Best Novel", "slug": "best-novel"},
        # Content will be rich text format
        "content": r'<h2 style="text-align: center;"><em>Chapter1: Hello world</em></h2><p>&nbsp;</p><p><em>Hello</em>, <span style="text-decoration: underline;"><strong>World!</strong></span></p>',
    }
    # look for chapter that created before current chapter with same novel id
    prev: dict = {
        "name": "CHAPTER 00",
        "novel": {"name": "Best Novel", "slug": "best-novel"},
        "slug": "chapter-00",
    }
    # look for chapter that created after current chapter with same novel id
    next: dict = {
        "name": "CHAPTER 02",
        "novel": {"name": "Best Novel", "slug": "best-novel"},
        "slug": "chapter-02",
    }
    return render_template("starter/chapter.html", chapter=chapter, prev=prev, next=next)
