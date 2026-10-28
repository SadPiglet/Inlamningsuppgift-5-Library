import sqlite3


def initialize_database():
  connection = None

  try:
    connection = sqlite3.connect("library.db")
    connection.execute("PRAGMA foreign_keys = ON")
    create_tables(connection)
    print("Library database connected and tables created successfully")
    connection.commit()

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
    total_copies INTEGER NOT NULL CHECK (total_copies >= 0)
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