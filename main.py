from book import Book
from database import initialize_database, add_book, book_exists
import sqlite3

books = [
  Book("The Tokyo Zodiac Murders", "Soji Shimada", 2024, 1, "9781805335153"),
  Book("I Am a Cat", "Natsume Sōseki", 2002, 1, "9780804832656"),
  Book("Strange Pictures", "Uketsu", 2025, 1, "9781805335399"),
  Book("The Honjin Murders", "Seishi Yokomizo", 2026, 1, "9781805336549"),
  Book("Letters from the Ginza Shihodo Stationery Shop", "Kenji Ueda", 2024, 1, "9781786584649")
]

initialize_database()

connection = sqlite3.connect("library.db")
connection.execute("PRAGMA foreign_keys = ON")

for book in books:
  if not book_exists(connection, book):
    add_book(connection, book)

connection.close()