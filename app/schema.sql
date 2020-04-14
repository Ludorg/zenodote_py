
DROP TABLE IF EXISTS books;

CREATE TABLE books (
  isbn INTEGER PRIMARY KEY,  
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  cover TEXT,
  publish_date TEXT,
  json_data JSON NOT NULL,
  book_url TEXT,
  author_url TEXT,
  ol_gb_type INTEGER
);

-- COMMIT;
