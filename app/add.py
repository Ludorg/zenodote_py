#
# Project: Zenodote
# Filename: add.py
# by Ludorg.Net (Ludovic LIEVRE) 2019/11/09
# https://ludorg.net/
#
# This work is licensed under the MIT License.
# See the LICENSE file in the root directory of this source tree.
#


import sys
import sqlite3
import json
import requests
from book import ol_Book, gb_Book
from isbn_ol import ol_request
from isbn_gb import gb_request

# logging stuff (requires verboselogs and coloredlogs)
# pip install verboselogs
# pip install coloredlogs
import logging
import verboselogs
import coloredlogs
logger = None
coloredlogs.install(level='DEBUG')  # , fmt='%(message)s')
verboselogs.install()
logger = logging.getLogger(__file__)
print = logger.debug
# end logging stuff


def add_book_to_db(isbn):
    """Add details on book in SQLite3 database from ISBN number (isbn) with data from openlibrary.org or Google Books if not found

    Database file is ./instance/zndt.sqlite
    ./instance/ folder comes from Flask deployement

    Images from cover (if any) is downloaded into ./instance/img_data/<isbn>

    """
    req_ok = False
    try:
        b = ol_request(isbn)
        req_ok = True
    except LookupError as e:
        logger.warning(e)

    if req_ok == False:
        try:
            b = gb_request(isbn)
            req_ok = True
        except LookupError as e2:
            logger.warning(e2)
            raise e2

    print(b)

    # dl image in instance/img_data
    if b.cover != None:
        download_cover(isbn, b.cover)

    con = sqlite3.connect("./instance/zndt.sqlite",
                          detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()

    cur.execute("INSERT OR REPLACE INTO books VALUES(?,?,?,?,?,?,?,?,?)", (b.isbn,
                                                                           b.author, b.title, b.cover, b.date, json.dumps(b.json_data), b.book_url, b.author_url, b.type.value))
    con.commit()
    con.close()

    logger.success('book %s added to database', isbn)

    pass


def download_cover(isbn, cover):
    # fixme wget is broken when installed with venv...
    # import wget
    # local_image_filename = wget.download(cover)

    import requests
    import shutil
    import os

    image_url = cover
    print(cover)

    resp = requests.get(image_url, stream=True)
    img_path = './app/static/img_data/' + str(isbn) + '/'
    print(img_path)

    os.makedirs(img_path, exist_ok=True)

    img_path = img_path + 'local_image.jpg'
    local_file = open(img_path, 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)

    logger.success('cover image for book %s saved as %s', isbn, img_path)
    del resp

    pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        add_book_to_db(sys.argv[1])
    else:
        logger.error("please provide isbn number (ISBN10 or ISBN13)")
