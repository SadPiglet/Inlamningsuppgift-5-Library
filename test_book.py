from book import Book
import unittest

class TestBook(unittest.TestCase):
  def test_book_initialization(self):
    # Test valid initialization
    book1 = Book("The Hobbit", "J. R. R. Tolkien", 1937, 5)

    self.assertEqual(book1.title, "The Hobbit")
    self.assertEqual(book1.author, "J. R. R. Tolkien")
    self.assertEqual(book1.publication_year, 1937)
    self.assertEqual(book1.total_copies, 5)

  # == INVALID TITLE TESTS ==
  def test_book_initialization_invalid_title(self):
    # Test invalid title (not a string)
    with self.assertRaises(TypeError):
      Book(123, "J. R. R. Tolkien", 1937, 5)

    # Test invalid title (empty string)
    with self.assertRaises(ValueError):
      Book("", "J. R. R. Tolkien", 1937, 5)

    # Test invalid title (string with only whitespace)
    with self.assertRaises(ValueError):
      Book("   ", "J. R. R. Tolkien", 1937, 5)


  # == INVALID AUTHOR TESTS ==
  def test_book_initialization_invalid_author(self):
    # Test invalid author (not a string)
    with self.assertRaises(TypeError):
      Book("The Hobbit", 123, 1937, 5)

    # Test invalid author (empty string)
    with self.assertRaises(ValueError):
      Book("The Hobbit", "", 1937, 5)


  # == INVALID PUBLICATION YEAR TESTS ==
  def test_book_initialization_invalid_publication_year(self):
    # Test invalid publication year (not an integer)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", "1937", 5)

    # Test invalid publication year (negative integer)
    with self.assertRaises(ValueError):
      Book("The Hobbit", "J. R. R. Tolkien", -1937, 5)

    # Test invalid publication year (zero)
    with self.assertRaises(ValueError):
      Book("The Hobbit", "J. R. R. Tolkien", 0, 5)    

    # Test invalid publication year (Boolean value)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", True, 5)

    # Test invalid publication year (float value)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937.5, 5)


  # == INVALID TOTAL COPIES TESTS ==   
  def test_book_initialization_invalid_total_copies(self):
    # Test invalid total copies (not an integer)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937, "5")

    # Test invalid total copies (negative integer)
    with self.assertRaises(ValueError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937, -5)

    # Test invalid copies (float)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937, 2.5)

    # Test invalid copies (Boolean)
    with self.assertRaises(TypeError):
      Book("The Hobbit", "J. R. R. Tolkien", 1937, True)

  # == VALID COPIES TEST ==
  def test_book_initialization_valid_total_copies_zero(self):
    # Test valid total copies (zero)
    book2 = Book("The Hobbit", "J. R. R. Tolkien", 1937, 0)

    self.assertEqual(book2.total_copies, 0)


  # == VALID TITLE/AUTHOR TEST ==
  def test_book_initialization_valid_title_and_author_with_whitespace(self):
    # Test valid title and author with leading/trailing whitespace
    book3 = Book("  The Hobbit  ", "  J. R. R. Tolkien  ", 1937, 5)

    self.assertEqual(book3.title, "The Hobbit")
    self.assertEqual(book3.author, "J. R. R. Tolkien")