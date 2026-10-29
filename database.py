
import sqlite3
from datetime import date


def initialize_database():
  connection = None

  try:
    connection = sqlite3.connect("library.db")
    connection.execute("PRAGMA foreign_keys = ON")
    create_tables(connection)
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


def calculate_age(date_of_birth):
  birth_date = date.fromisoformat(date_of_birth)
  today = date.today()

  age = today.year - birth_date.year

  if (today.month, today.day) < (birth_date.month, birth_date.day):
    age -= 1

  return age

def generate_personal_number(connection, date_of_birth):
  date_parts = date_of_birth.split("-")

  year = date_parts[0]
  month = date_parts[1]
  day = date_parts[2]

  date_prefix = f"{year[-2:]}{month}{day}"

  cursor = connection.execute("""
    SELECT personal_number
    FROM Users
    WHERE personal_number LIKE ?
  """, (f"{date_prefix}-%",))

  existing_numbers = {
    int(row[0].split("-")[1])
    for row in cursor.fetchall()
  }

  for number in range(10000):
    if number not in existing_numbers:
      return f"{date_prefix}-{number:04d}"

  raise ValueError("No available personal numbers for this date.")

def add_user(connection, first_name, last_name, date_of_birth):
  first_name = validate_name(first_name, "First name")
  last_name = validate_name(last_name, "Last name")
  date_of_birth = validate_date_of_birth(date_of_birth)

  personal_number = generate_personal_number(connection, date_of_birth)

  connection.execute("""
    INSERT INTO Users (
    first_name,
    last_name,
    date_of_birth,
    personal_number
    )
    VALUES (?, ?, ?, ?)
  """, (first_name, last_name, date_of_birth, personal_number))

  connection.commit()

  return personal_number

# === GET ALL USERS ===
def get_all_users(connection):
  cursor = connection.execute("""
    SELECT user_id, first_name, last_name, date_of_birth, personal_number
    FROM Users
    ORDER by last_name, first_name
  """)

  return cursor.fetchall()


# === GET USER BY PERSONAL NUMBER ===
def get_user_by_personal_number(connection, personal_number):
  cursor = connection.execute("""
    SELECT user_id, first_name, last_name, date_of_birth, personal_number
    FROM Users
    WHERE personal_number = ?
  """, (personal_number,))

  return cursor.fetchone()


# === DELETE USER ===
def delete_user(connection, user_id):
  cursor = connection.execute("""
    SELECT 1
    FROM Loans
    WHERE user_id = ?
    AND return_date IS NULL
  """, (user_id,))

  if cursor.fetchone() is not None:
    raise ValueError("Cannot delete a user with active loans.")

  cursor = connection.execute("""
    SELECT 1
    FROM Users
    WHERE user_id = ?
  """, (user_id,))

  if cursor.fetchone() is None:
    raise ValueError("User not found.")

  connection.execute("""
    DELETE FROM Loans
    WHERE user_id = ?
  """, (user_id,))

  connection.execute("""
    DELETE FROM Users
    WHERE user_id = ?
  """, (user_id,))

  connection.commit()

# == Validate name ==
def validate_name(name, field_name):
  if not isinstance(name, str):
    raise TypeError(f"{field_name} must be a string")

  if not name.strip():
    raise ValueError(f"{field_name} cannot be empty")

  return name.strip()

# == Validate birthday ==
def validate_date_of_birth(date_of_birth):
  if not isinstance(date_of_birth, str):
    raise TypeError("Date of birth must be a string")

  try:
    birth_date = date.fromisoformat(date_of_birth)
  except ValueError:
    raise ValueError("Date of birth must use YYYY-MM-DD format")

  if birth_date > date.today():
    raise ValueError("Date of birth cannot be in the future")

  return birth_date.isoformat()
