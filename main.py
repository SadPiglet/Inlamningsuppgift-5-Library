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
  delete_user
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
    print("Q. Exit")

    choice = input("Choose an option: ").strip().lower()

    if choice == "1":
      user_management_menu(connection)
    elif choice == "2":
      print("Borrow a Book - WIP")
    elif choice == "3":
      print("Loans Management - WIP")
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
    first_name = get_user_input(
      "Enter your first name (or Q to quit): "
    )
    if first_name is None:
      print("Registration cancelled.")
      return

    last_name = get_user_input(
      "Enter your last name (or Q to quit): "
    )
    if last_name is None:
      print("Registration cancelled.")
      return

    date_of_birth = get_user_input(
      "Enter your date of birth (YYYY-MM-DD, or Q to quit): "
    )
    if date_of_birth is None:
      print("Registration cancelled.")
      return

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