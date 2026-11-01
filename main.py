# === IMPORTS ===
from book import Book
import sqlite3

from database import (
  initialize_database,
  add_book,
  book_exists,
  add_user,
  calculate_age,
  get_all_users,
  get_user_by_personal_number,
  delete_user,
  get_all_books,
  get_book_by_isbn,
  borrow_book,
  get_user_active_loans,
  get_all_active_loans,
  return_book,
  validate_date_of_birth

)


# === BOOK COLLECTION ===
books = [
  Book("The Tokyo Zodiac Murders", "Soji Shimada", 2024, 1, "9781805335153"),
  Book("I Am a Cat", "Natsume Sōseki", 2002, 1, "9780804832656"),
  Book("Strange Pictures", "Uketsu", 2025, 1, "9781805335399"),
  Book("The Honjin Murders", "Seishi Yokomizo", 2026, 1, "9781805336549"),
  Book(
    "Letters from the Ginza Shihodo Stationery Shop",
    "Kenji Ueda",
    2024,
    1,
    "9781786584649"
  )
]


# === USER INPUT ===
def get_user_input(prompt):
  value = input(prompt)

  if value.strip().lower() == "q":
    return None

  return value


# === MAIN MENU ===
def main_menu(connection):
  while True:
    print("\n=== Library Management System ===")
    print("1. User Management")
    print("2. Borrow a Book")
    print("3. Loans Management")
    print("4. Return a Book")
    print("Q. Exit")

    choice = input("Choose an option: ").strip().lower()

    if choice == "1":
      user_management_menu(connection)
    elif choice == "2":
      borrow_a_book(connection)
    elif choice == "3":
      loans_management_menu(connection)
    elif choice == "4":
      return_a_book(connection)
    elif choice == "q":
      print("Exiting library system. Goodbye!")
      break
    else:
      print("Invalid choice. Please try again.")


# === USER MANAGEMENT MENU ===
def user_management_menu(connection):
  while True:
    print("\n === User Management ===")
    print("1. Register a user")
    print("2. View all users")
    print("3. View user details")
    print("4. Remove a user")
    print("Q. Back to main menu")

    choice = input("Choose an option: ").strip().lower()

    if choice == "1":
      register_user(connection)
    elif choice == "2":
      view_all_users(connection)
    elif choice == "3":
      view_user_details(connection)
    elif choice == "4":
      remove_user(connection)
    elif choice == "q":
      break
    else:
      print("Invalid choice. Please try again.")


# === USER REGISTRATION ===
def register_user(connection):
  try:
    # Collect user details
    while True:
      first_name = get_user_input(
        "Enter your first name (or Q to quit): "
      )
      
      if first_name is None:
        print("Registration cancelled.")
        return

      first_name = first_name.strip()

      if first_name:
        break

      print("First name cannot be empty.")

    while True:
      last_name = get_user_input(
        "Enter your last name (or Q to quit): "
      )
      
      if last_name is None:
        print("Registration cancelled.")
        return

      last_name = last_name.strip()

      if last_name:
        break

      print("Last name cannot be empty.")

    while True:
      date_of_birth = get_user_input(
        "Enter your date of birth (YYYY-MM-DD, or Q to quit): "
      )
      
      if date_of_birth is None:
        print("Registration cancelled.")
        return

      date_of_birth = date_of_birth.strip()

      if not date_of_birth:
        print("Date of birth cannot be empty.")
        continue

      try:
        date_of_birth = validate_date_of_birth(date_of_birth)
        break
      except ValueError as error:
        print(f"Invalid date of birth: {error}")


    # Save the user and retrieve their personal number
    personal_number = add_user(
      connection,
      first_name,
      last_name,
      date_of_birth
    )

    # Confirm successful registration
    print(
      f"User registered successfully! "
      f"Personal number: {personal_number}"
    )

  except ValueError as error:
    print(f"Registration failed: {error}")
    print("Please try again.")


# === VIEW ALL USERS ===
def view_all_users(connection):
  users = get_all_users(connection)

  if not users:
    print("No users registered.")
    return

  print("=== Registered Users ===")

  for user in users:
    user_id, first_name, last_name, date_of_birth, personal_number = user
    print(f"{first_name} {last_name} | Personal number: {personal_number}")


# === VIEW USER DETAILS ===
def view_user_details(connection):
  personal_number = input(
    "Enter the user's personal number (or Q to cancel): "
  ).strip()

  if personal_number.lower() == "q":
    return

  user = get_user_by_personal_number(connection, personal_number)

  if user is None:
    print("User not found.")
    return

  user_id, first_name, last_name, date_of_birth, personal_number = user
  age = calculate_age(date_of_birth)

  print("\n=== User Details ===")
  print(f"First name: {first_name}")
  print(f"Last name: {last_name}")
  print(f"Date of birth: {date_of_birth}")
  print(f"Age: {age}")
  print(f"Personal number: {personal_number}")


# === REMOVE USER ===
def remove_user(connection):
  personal_number = input(
    "Enter the user's personal number to remove (or Q to cancel): "
  ).strip()

  if personal_number.lower() == "q":
    return

  user = get_user_by_personal_number(connection, personal_number)

  if user is None:
    print("User not found.")
    return

  user_id, first_name, last_name, date_of_birth, personal_number = user

  print(f"User: {first_name} {last_name}")
  confirmation = input("Are you sure you want to remove this user? (y/n): ")

  if confirmation.strip().lower() != "y":
    print("Removal cancelled.")
    return

  try:
    delete_user(connection, user_id)
    print("User removed successfully!")
  except ValueError as error:
    print(f"Could not remove user: {error}")


# === BORROW A BOOK ===
def borrow_a_book(connection):
  available_books = []

  for book in get_all_books(connection):
    book_id, title, author, publication_year, total_copies, isbn = book

    active_loans = connection.execute("""
      SELECT COUNT(*)
      FROM Loans
      WHERE book_id = ?
      AND return_date IS NULL
    """, (book_id,)).fetchone()[0]

    if active_loans < total_copies:
      available_books.append(book)

  if not available_books:
    print("No books are currently available to borrow.")
    return

  print("\n=== Available Books ===")

  for index, book in enumerate(available_books, start=1):
    book_id, title, author, publication_year, total_copies, isbn = book
    print(f"{index}. {title} by {author} ({publication_year}) | ISBN: {isbn}")

  choice = get_user_input("Choose a book number (or Q to cancel): ")

  if choice is None:
    print("Borrowing cancelled.")
    return

  if not choice.isdigit():
    print("Invalid choice.")
    return

  book_index = int(choice) -1

  if book_index < 0 or book_index >= len(available_books):
    print("Invalid book number.")
    return

  book = available_books[book_index]

  personal_number = get_user_input(
    "Enter the borrower's personal number (or Q to cancel): "
  )

  if personal_number is None:
    print("Borrowing cancelled.")
    return

  user = get_user_by_personal_number(connection, personal_number.strip())

  if user is None:
    print("User not found.")
    return

  book_id = book[0]
  user_id = user[0]

  try:
    borrow_book(connection, book_id, user_id)
    print(
      f"Book '{book[1]}' successfully borrowed by "
      f"{user[1]} {user[2]}!"
    )
  except ValueError as error:
    print(f"Could not borrow book: {error}")


# === LOANS MANAGEMENT MENU ===
def loans_management_menu(connection):
  while True:
    print("\n=== Loans Management ===")
    print("1. View a user's loans")
    print("2. View all active loans")
    print("Q. Back to main menu")

    choice = input("Choose an option: ").strip().lower()

    if choice == "1":
      view_user_loans(connection)
    elif choice == "2":
      view_all_loans(connection)
    elif choice == "q":
      break
    else:
      print("Invalid choice. Please try again.")


# === VIEW USERS LOANS ===
def view_user_loans(connection):
  personal_number = get_user_input(
    "Enter the user's personal number (or Q to cancel): "
  )

  if personal_number is None:
    print("Search cancelled.")
    return

  user = get_user_by_personal_number(connection, personal_number.strip())

  if user is None:
    print("User not found.")
    return

  user_id, first_name, last_name, date_of_birth, personal_number = user
  loans = get_user_active_loans(connection, user_id)

  print(f"\n=== Active loans for {first_name} {last_name} ===")

  if not loans:
    print("This user has no active loans.")
    return

  for loan in loans:
    book_id, title, author, loan_date = loan
    print(f"{title} by {author} | Loan date: {loan_date}")


# === RETURN BOOK ===
def return_a_book(connection):
  personal_number = get_user_input(
    "Enter your personal number (or Q to cancel): "
  )

  if personal_number is None:
    print("Return cancelled.")
    return

  user = get_user_by_personal_number(connection, personal_number.strip())

  if user is None:
    print("User not found.")
    return

  loans = connection.execute("""
    SELECT Loans.loan_id, Books.title, Books.author, Loans.loan_date
    FROM Loans
    JOIN Books ON Loans.book_id = Books.book_id
    WHERE Loans.user_id = ?
    AND Loans.return_date IS NULL
  """, (user[0],)).fetchall()

  if not loans:
    print("You have no active loans.")
    return

  print("\n=== Your Active Loans ===")

  for index, loan in enumerate(loans, start=1):
    print(f"{index}. {loan[1]} by {loan[2]} | Loan date: {loan[3]}")

  choice = get_user_input(
    "Choose a loan number to return (or Q to cancel): "
  )

  if choice is None:
    print("Return cancelled.")
    return

  if not choice.isdigit() or not 1 <= int(choice) <= len(loans):
    print("Invalid choice.")
    return

  loan_id = loans[int(choice) - 1][0]

  try:
    return_book(connection, loan_id)
    print("Book returned successfully!")
  except ValueError as error:
    print(f"Could not return book: {error}")

# === VIEW ALL LOANS ===
def view_all_loans(connection):
  loans = get_all_active_loans(connection)

  print("\n=== All Active Loans ===")

  if not loans:
    print("There are no active loans.")
    return

  for loan in loans:
    first_name, last_name, personal_number, title, author, loan_date = loan

    print(
      f"{title} by {author} | "
      f"Borrower: {first_name} {last_name} "
      f"({personal_number}) | Loan date: {loan_date}"
    )



# === APPLICATION SETUP AND EXECUTION ===
def main():
  # Initialize the database
  initialize_database()

  # Open the database connection
  connection = sqlite3.connect("library.db")
  connection.execute("PRAGMA foreign_keys = ON")

  try:
    # Add the initial books if they do not already exist
    for book in books:
      if not book_exists(connection, book):
        add_book(connection, book)

    # Start the main menu
    main_menu(connection)

  finally:
    # Always close the database connection
    connection.close()


# === PROGRAM ENTRY POINT ===
if __name__ == "__main__":
  main()