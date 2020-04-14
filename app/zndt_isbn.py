#
# Project: Zenodote
# Filename: zndt_isbn.py
# by Ludorg.Net (Ludovic LIEVRE) 2019/11/10
# https://ludorg.net/
#
# This work is licensed under the MIT License.
# See the LICENSE file in the root directory of this source tree.
#

from app.db import get_db
from flask import Blueprint
from flask import render_template
from flask import Flask

bp = Blueprint("zndt_isbn", __name__)

BOOKS_PER_PAGE = 7


@bp.route("/")
def index():
    return render_page(1)


@bp.route("/page/<int:page>")
def render_page(page):
    """Show all the isbn books for page
    page number start at 1 
    """
    if page < 1:
        page = 1
    db = get_db()
    books = db.execute(
        "SELECT isbn, author, title"
        " FROM books LIMIT ? OFFSET ?", (str(
            BOOKS_PER_PAGE), str(BOOKS_PER_PAGE*(page-1)))
    ).fetchall()

    nb_books = db.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()

    if int(nb_books[0]) % BOOKS_PER_PAGE != 0:
        ptot = 1 + int(nb_books[0]) // BOOKS_PER_PAGE
    else:
        ptot = int(nb_books[0]) // BOOKS_PER_PAGE

    return render_template("index.html", ol_books=books, page=page, page_total=ptot)


@bp.route("/book/<int:isbn>")
def book_isbn(isbn):
    """Show one isbn book"""
    db = get_db()
    b = db.execute(
        "SELECT isbn, author, title, publish_date, book_url, ol_gb_type"
        " FROM books WHERE isbn=?", (isbn,)
    ).fetchone()
    c = '/static/img_data/' + str(isbn) + '/local_image.jpg'
    return render_template("book.html", book=b, cover=c, page=-1)
