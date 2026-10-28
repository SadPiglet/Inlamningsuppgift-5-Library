class Book:
  def __init__(self, title, author, publication_year, total_copies, isbn):

    # === Validate title ===
    if not isinstance(title, str):
      raise TypeError("Title must be a string")
    if not title.strip():
      raise ValueError("Title cannot be empty")

    # === Validate author ===
    if not isinstance(author, str):
      raise TypeError("Author must be a string")
    if not author.strip():
      raise ValueError("Author cannot be empty")

    # === Validate publication_year ===
    if type(publication_year) is not int:
      raise TypeError("Publication year must be an integer")
    if publication_year < 1:
      raise ValueError("Publication year must be a positive integer")

    # === Validate total_copies ===
    if type(total_copies) is not int:
      raise TypeError("Total copies must be an integer")
    if total_copies < 0:
      raise ValueError("Total copies cannot be negative")

    # === Validate ISBN ===
    if not isinstance(isbn, str):
      raise TypeError("ISBN must be a string")

    normalized_isbn = isbn.replace("-", "").replace(" ", "")

    if not normalized_isbn.isdigit():
      raise ValueError("ISBN must contain only digits and hyphens")

    if len(normalized_isbn) not in (10, 13):
      raise ValueError("ISBN must contain 10 or 13 digits")

    # === Assign attributes ===
    self.title = title.strip()
    self.author = author.strip()
    self.publication_year = publication_year
    self.total_copies = total_copies
    self.isbn = normalized_isbn