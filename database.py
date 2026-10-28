
import sqlite3


def initialize_database():
  connection = None

  try:
    connection = sqlite3.connect("library.db")
    connection.execute("PRAGMA foreign_keys = ON")
    create_tables(connection)
    migrate_books_isbn(connection)
    connection.commit()
    print("Library database connected and tables created successfully")

  finally:
    if connection is not None:
      connection.close()
      print("Library database connection has closed.")


def create_tables(connection):

  # === Books ===
  connection.execute("""
    CREATE TABLE IF NOT EXISTS Books (
      book_id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      author TEXT NOT NULL,
      publication_year INTEGER NOT NULL CHECK (publication_year >= 1),
      total_copies INTEGER NOT NULL CHECK (total_copies >= 0),
      isbn TEXT NOT NULL UNIQUE
    )
  """)

  # === Users ===
  connection.execute("""
    CREATE TABLE IF NOT EXISTS Users (
      user_id INTEGER PRIMARY KEY AUTOINCREMENT,
      first_name TEXT NOT NULL,
      last_name TEXT NOT NULL,
      date_of_birth TEXT NOT NULL,
      personal_number TEXT NOT NULL UNIQUE
    )
  """)

  # === Loans ===
  connection.execute("""
    CREATE TABLE IF NOT EXISTS Loans (
      loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
      book_id INTEGER NOT NULL,
      user_id INTEGER NOT NULL,
      loan_date TEXT NOT NULL,
      return_date TEXT,
      FOREIGN KEY (user_id) REFERENCES Users (user_id),
      FOREIGN KEY (book_id) REFERENCES Books (book_id)
    )
  """)


def migrate_books_isbn(connection):
  # Add ISBN to an existing Books table if it is missing.
  columns = connection.execute(
    "PRAGMA table_info(Books)"
  ).fetchall()

  column_names = [column[1] for column in columns]

  if "isbn" not in column_names:
    connection.execute("ALTER TABLE Books ADD COLUMN isbn TEXT")

  # ISBNs printed in the user's five existing books.
  existing_books = [
    (
      "The Tokyo Zodiac Murders",
      "Soji Shimada",
      "9781805335153"
    ),
    (
      "I Am a Cat",
      "Natsume Sōseki",
      "9780804832656"
    ),
    (
      "Strange Pictures",
      "Uketsu",
      "9781805335399"
    ),
    (
      "The Honjin Murders",
      "Seishi Yokomizo",
      "9781805336549"
    ),
    (
      "Letters from the Ginza Shihodo Stationery Shop",
      "Kenji Ueda",
      "9781786584649"
    )
  ]

  for title, author, isbn in existing_books:
    connection.execute("""
      UPDATE Books
      SET isbn = ?
      WHERE title = ?
        AND author = ?
        AND (isbn IS NULL OR isbn = '')
    """, (isbn, title, author))

  # Do not continue if any existing book is still missing an ISBN.
  missing_isbn = connection.execute("""
    SELECT COUNT(*)
    FROM Books
    WHERE isbn IS NULL OR TRIM(isbn) = ''
  """).fetchone()[0]

  if missing_isbn > 0:
    raise ValueError(
      f"{missing_isbn} book(s) are missing an ISBN. "
      "The database migration was stopped."
    )

  # Enforce ISBN uniqueness, including for the existing database.
  connection.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_books_isbn
    ON Books (isbn)
  """)


def add_book(connection, book):
  connection.execute("""
    INSERT INTO Books (
      title,
      author,
      publication_year,
      total_copies,
      isbn
    )
    VALUES (?, ?, ?, ?, ?)
  """, (
    book.title,
    book.author,
    book.publication_year,
    book.total_copies,
    book.isbn
  ))

  connection.commit()


def book_exists(connection, book):
  result = connection.execute("""
    SELECT 1
    FROM Books
    WHERE isbn = ?
  """, (book.isbn,))

  return result.fetchone() is not None
