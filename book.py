class Book:
  def __init__(self, title, author, publication_year, total_copies):

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

    # === Assign attributes ===
    self.title = title.strip()
    self.author = author.strip()
    self.publication_year = publication_year
    self.total_copies = total_copies