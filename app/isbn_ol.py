#
# Project: Zenodote
# Filename: isbn_ol.py
# by Ludorg.Net (Ludovic LIEVRE) 2019/05/13
# https://ludorg.net/
#
# This work is licensed under the MIT License.
# See the LICENSE file in the root directory of this source tree.
#

from book import ol_Book

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


def ol_request(isbn):
    """Finds details on book from ISBN number (isbn) on openlibrary.org

    Returns an ol_Book (py:class:: ol_Book) object containing
      - JSON raw result
      - Title of book
      - Book's author
      - If available, URL of large cover. None, if cover is not available
      - Publish date
      - URL to book on openlibrary.org page
      - URL to author on openlibrary.org page

    Raises LookupError if isbn is not found

    """
    url = 'https://openlibrary.org/api/books?bibkeys='
    url += 'ISBN:{0}&format=json&jscmd=data'.format(isbn)

    r = requests.get(url)
    print(r.content)

    if r.ok:
        j = r.json()
        root = 'ISBN:{0}'.format(isbn)
        logger.success('Request OK for %s', root)
        if root in j:
            logger.success('%s found', root)
            title = j[root]['title']
            if 'authors' in j[root]:
                author = j[root]['authors'][0]['name']
            else:
                author = 'Unknown author'
            cover = None
            if 'cover' in j[root]:
                cover = j[root]['cover']['large']
            link = j[root]['url']
            date = j[root]['publish_date']
            return ol_Book(isbn, author, title, cover, date, j, link)
        else:
            logger.error('%s not found', root)
            raise LookupError(isbn)


if __name__ == "__main__":
    i = 9782847200065
    b = ol_request(i)

    print(b)

    print(ol_request(9782253009689))
    # print(ol_request(9782322143191))
    # print(ol_request(9782956217459))
    # print(ol_request(123))
