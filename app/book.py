#
# Project: Zenodote
# Filename: book.py
# by Ludorg.Net (Ludovic LIEVRE) 2019/05/13
# https://ludorg.net/
#
# This work is licensed under the MIT License.
# See the LICENSE file in the root directory of this source tree.
#


from enum import Enum, auto
import sqlite3


# isbn numbers are 13 digits decimal => max 10^14 -1
# 64 bits should be enough

class Book:
    def __init__(self, isbn, author, title, cover):
        self.isbn = int(isbn)
        self.author = author
        self.title = title
        self.cover = cover
        self.type = None
        pass

    def __repr__(self):
        return "%i;%s;%s;%s;%s" % (self.isbn, self.author, self.title, self.cover, self.type)

    # def __conform__(self, protocol):
    #     if protocol is sqlite3.PrepareProtocol:
    #         return self.__repr__()


class BookType(Enum):
    OPEN_LIBRARY = auto()
    GOOGLE_BOOKS = auto()


class ol_Book(Book):
    def __init__(self, isbn, author, title, cover, date, json_data, book_url, author_url=None):
        super().__init__(isbn, author, title, cover)
        self.date = date
        self.json_data = json_data
        self.book_url = book_url
        self.author_url = author_url
        self.type = BookType.OPEN_LIBRARY
        pass


class gb_Book(ol_Book):
    def __init__(self, isbn, author, title, cover, date, json_data, book_url, author_url=None):
        super().__init__(isbn, author, title, cover, date, json_data, book_url, author_url)
        self.type = BookType.GOOGLE_BOOKS  # override type
        pass

    # def __conform__(self, protocol):
    #     if protocol is sqlite3.PrepareProtocol:
    #         return self.__repr__()


# if __name__ == "__main__":
#     con = sqlite3.connect("zndt_test.db", detect_types=sqlite3.PARSE_DECLTYPES)
#     cur = con.cursor()

#     b = ol_Book(9782847200065, "aaa", "ttt", "ccc", "2019/11/09", "{ISBN:\"9782847200065\"}", "https://openlibrary.org/books/OL12627293M/aaa")
#     cur.execute("INSERT INTO ol_books VALUES(?,?,?,?,?,?,?,?,?)", (b.isbn, b.author, b.title, b.cover, b.date, b.json_data, b.book_url, b.book_url))
#     con.commit()
#     isbn = 9782847200065
#     author = 'aaa'
#     cur.execute("SELECT author FROM ol_books WHERE isbn=?", (isbn,))
#     for row in cur:
#         # row[0] returns the first column in the query (name), row[1] returns email column.
#         print('{0}'.format(row[0]))

#     #con = sqlite3.connect("zndt_test.db")
#     #cur = con.cursor()

#     #cur.execute("select ?", (b,))
#     # print(cur.fetchone()[0])

#     con.close()
