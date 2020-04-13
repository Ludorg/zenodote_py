#
# Project: Zenodote
# Filename: book_test.py
# by Ludorg.Net (Ludovic LIEVRE) 2019/05/13
# https://ludorg.net/
#
# This work is licensed under the
# Creative Commons Attribution 4.0 International License.
# To view a copy of this license,
# visit https://creativecommons.org/licenses/by/4.0/.
#


import unittest
from book import Book, ol_Book, gb_Book, BookType


class BookTestCase(unittest.TestCase):
    def test_construct(self):
        b = Book(9782847200065, "aaa", "bbb", "ccc")
        self.assertEqual(b.isbn, 9782847200065)
        self.assertEqual(b.author, "aaa")
        self.assertEqual(b.title, "bbb")
        self.assertEqual(b.cover, "ccc")

    def test_construct_ol(self):
        b = ol_Book(9782847200065, "aaa", "bbb", "ccc", "2019/11/09",
                    "{ISBN:\"9782847200065\"}", "https://openlibrary.org/books/OL12627293M/aaa")
        self.assertEqual(b.isbn, 9782847200065)
        self.assertEqual(b.author, "aaa")
        self.assertEqual(b.title, "bbb")
        self.assertEqual(b.cover, "ccc")
        self.assertEqual(b.json_data, "{ISBN:\"9782847200065\"}")
        self.assertEqual(
            b.book_url, "https://openlibrary.org/books/OL12627293M/aaa")
        
        self.assertEqual(b.type, BookType.OPEN_LIBRARY)

        print(b)

        
    def test_construct_gb(self):
        b = gb_Book(9782847200065, "aaa", "bbb", "ccc", "2019/11/09",
                    "{ISBN:\"9782847200065\"}", "https://openlibrary.org/books/OL12627293M/aaa")
        self.assertEqual(b.isbn, 9782847200065)
        self.assertEqual(b.author, "aaa")
        self.assertEqual(b.title, "bbb")
        self.assertEqual(b.cover, "ccc")
        self.assertEqual(b.json_data, "{ISBN:\"9782847200065\"}")
        self.assertEqual(
            b.book_url, "https://openlibrary.org/books/OL12627293M/aaa")
        
        self.assertEqual(b.type, BookType.GOOGLE_BOOKS)

        print(b)


if __name__ == '__main__':
    unittest.main()
