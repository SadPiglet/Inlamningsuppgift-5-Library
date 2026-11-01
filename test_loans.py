import sqlite3
import unittest

from database import create_tables, add_book, borrow_book
from book import Book


class TestBookLoans(unittest.TestCase):

  def setUp(self):
    self.connection = sqlite3.connect(":memory:")
    self.connection.execute("PRAGMA foreign_keys = ON")
    create_tables(self.connection)

    book = Book(
      "Test Book",
      "Test Author",
      2024,
      1,
      "9781234567897"
    )
    add_book(self.connection, book)

    self.connection.execute("""
      INSERT INTO Users (
        first_name, last_name, date_of_birth, personal_number
        )
      VALUES ('Test', 'User', '2000-01-01', '000101-0001')
    """)
    self.connection.commit()

    self.book_id = self.connection.execute(
      "SELECT book_id FROM Books"
    ).fetchone()[0]

    self.user_id = self.connection.execute(
      "SELECT user_id FROM Users"
    ).fetchone()[0]

  def tearDown(self):
    self.connection.close()

  def test_borrow_book_successfully(self):
    borrow_book(self.connection, self.book_id, self.user_id)

    loan = self.connection.execute("""
    SELECT book_id, user_id, return_date
    FROM Loans
    """).fetchone()

    self.assertEqual(loan, (self.book_id, self.user_id, None))

  def test_cannot_borrow_unavailable_book(self):
    borrow_book(self.connection, self.book_id, self.user_id)

    with self.assertRaises(ValueError):
      borrow_book(self.connection, self.book_id, self.user_id)

if __name__ == "__main__":
  unittest.main()