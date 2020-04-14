#
# Project: Zenodote
# Filename: isbn_gb.py
# by Ludorg.Net (Ludovic LIEVRE) 2019/11/12
# https://ludorg.net/
#
# This work is licensed under the MIT License.
# See the LICENSE file in the root directory of this source tree.
#

from book import gb_Book

import requests

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


def gb_request(isbn):
    """Finds details on book from ISBN number (isbn) on Google Books

    Returns a gb_Book (py:class:: gb_Book) object containing
      - JSON raw result
      - Title of book
      - Book's author
      - If available, URL of large cover. None, if cover is not available
      - Publish date
      - URL to book on openlibrary.org page
      - URL to author on openlibrary.org page
      - type set to BookType.GOOGLE_BOOKS

    Raises LookupError if isbn is not found

    """

    url = 'https://www.googleapis.com/books/v1/volumes?q='
    url += 'isbn:{0}'.format(isbn)

    print(url)

    r = requests.get(url)
    print(r.content)

    if r.ok:
        root = 'ISBN:{0}'.format(isbn)
        logger.success('Request OK for %s', root)

        j = r.json()
        if j['totalItems'] == 0:
            logger.error('%s not found', root)
            raise LookupError(isbn)
        else:
            logger.success('%s found', root)

            title = j['items'][0]['volumeInfo']['title']
            if 'authors' in j['items'][0]['volumeInfo']:
                author = j['items'][0]['volumeInfo']['authors'][0]
            else:
                author = 'Unknown author'

            cover = None
            if 'imageLinks' in j['items'][0]['volumeInfo']:
                if 'thumbnail' in j['items'][0]['volumeInfo']['imageLinks']:
                    cover = j['items'][0]['volumeInfo']['imageLinks']['thumbnail']
                    cover = cover.replace('zoom=1', 'zoom=2')

            date = j['items'][0]['volumeInfo']['publishedDate']
            link = j['items'][0]['volumeInfo']['previewLink']
            return gb_Book(isbn, author, title, cover, date, j, link)


if __name__ == "__main__":
    i = 9782020104821
    # 9782847200065 not present on google books

    b = gb_request(i)

    print(b)

    print(gb_request(9782253009689))
    # print(ol_request(9782322143191))
    # print(ol_request(9782956217459))
    # print(ol_request(123))
