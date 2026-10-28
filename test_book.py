from book import Book
import unittest

VALID_ISBN = "9780804832656"

class TestBook(unittest.TestCase):
  def test_book_initialization(self):
    # Test valid initialization
    book1 = Book("The Hobbit", "J. R. R. Tolkien", 1937, 5, VALID_ISBN)

    self.assertEqual(book1.title, "The Hobbit")
    self.assertEqual(book1.author, "J. R. R. Tolkien")
    self.assertEqual(book1.publication_year, 1937)
    self.assertEqual(book1.total_copies, 5)
    self.assertEqual(book1.isbn, VALID_ISBN)

  # == INVALID TITLE TESTS ==
  def test_book_initialization_invalid_title(self):
    # Test invalid title (not a string)
    with self.assertRaises(TypeError):
      Book(123, "J. R. R. Tolkien", 1937, 5, VALID_ISBN)

    # Test invalid title (empty string)
    with self.assertRaises(ValueError):
      Book("", "J. R. R. Tolkien", 1937, 5, VALID_ISBN)

    # Test invalid title (string with only whitespace)
    with self.assertRaises(ValueError):
      Book("   ", "J. R. R. Tolkien", 1937, 5, VALID_ISBN)


  # == INVALID AUTHOR TESTS ==
  def test_book_initialization_invalid_author(self):
    # Test invalid author (not a string)
    with self.assertRaises(TypeError):
      Book("The Hobbit", 123, 1937, 5, VALID_ISBN)

    # Test invalid author (empty string)
    with self.assertRaises(ValueError):
      Book("The Hobbit", "", 1937, 5, VALID_ISBN)


  # == INVALID PUBLICATION YEAR TESTS ==
  def test_book_initialization_invalid_publication_year(self):
    # Test invalid publication year (not an integer)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", "1937", 5, VALID_ISBN)

    # Test invalid publication year (negative integer)
    with self.assertRaises(ValueError):
      Book("The Hobbit", "J. R. R. Tolkien", -1937, 5, VALID_ISBN)

    # Test invalid publication year (zero)
    with self.assertRaises(ValueError):
      Book("The Hobbit", "J. R. R. Tolkien", 0, 5, VALID_ISBN)    

    # Test invalid publication year (Boolean value)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", True, 5, VALID_ISBN)

    # Test invalid publication year (float value)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937.5, 5, VALID_ISBN)


  # == INVALID TOTAL COPIES TESTS ==   
  def test_book_initialization_invalid_total_copies(self):
    # Test invalid total copies (not an integer)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937, "5", VALID_ISBN)

    # Test invalid total copies (negative integer)
    with self.assertRaises(ValueError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937, -5, VALID_ISBN)

    # Test invalid copies (float)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937, 2.5, VALID_ISBN)

    # Test invalid copies (Boolean)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937, True, VALID_ISBN)


  # == INVALID ISBN TEST ==
  def test_book_initialization_invalid_isbn_type(self):
    # Test invalid ISBN (not a string)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937, 5, 12345)

    # Test invalid ISBN (contains letters)
    with self.assertRaises(ValueError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937, 5, "ABC123")

    # Test invalid ISBN (incorrect number of digits)
    with self.assertRaises(ValueError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937, 5, "12345")
      

  # == VALID ISBN TEST ==
  def test_book_initialization_valid_isbn_with_hyphens(self):
    # Test valid ISBN (hyphens are removed)
    book = Book("The Hobbit", "J. R. R. Tolkien", 1937, 5, "978-0-8048-3265-6")

    self.assertEqual(book.isbn, "9780804832656")


  # == VALID COPIES TEST ==
  def test_book_initialization_valid_total_copies_zero(self):
    # Test valid total copies (zero)
    book2 = Book("The Hobbit", "J. R. R. Tolkien", 1937, 0, VALID_ISBN)

    self.assertEqual(book2.total_copies, 0)


  # == VALID TITLE/AUTHOR TEST ==
  def test_book_initialization_valid_title_and_author_with_whitespace(self):
    # Test valid title and author with leading/trailing whitespace
    book3 = Book("  The Hobbit  ", "  J. R. R. Tolkien  ", 1937, 5, VALID_ISBN)

    self.assertEqual(book3.title, "The Hobbit")
    self.assertEqual(book3.author, "J. R. R. Tolkien")