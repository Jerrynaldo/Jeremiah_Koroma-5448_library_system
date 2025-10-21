# operations.py

GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Fantasy", "Mystery", "Biography")

books = {}
members = []


# Find member by ID
def _find_member(member_id):
    for m in members:
        if m["member_id"] == member_id:
            return m
    return None


# Check if ISBN exists
def _book_exists(isbn):
    return isbn in books


# 2. Core Functions

def add_book(isbn, title, author, genre, total_copies):
    if genre not in GENRES:
        raise ValueError(f"Invalid genre: {genre}. Must be one of {GENRES}")
    if _book_exists(isbn):
        raise ValueError(f"Book with ISBN {isbn} already exists.")
    if total_copies < 0:
        raise ValueError("Total copies cannot be negative.")
    books[isbn] = {
        "title": title,
        "author": author,
        "genre": genre,
        "total_copies": total_copies
    }


def add_member(member_id, name, email):
    if _find_member(member_id):
        raise ValueError(f"Member with ID {member_id} already exists.")
    members.append({
        "member_id": member_id,
        "name": name,
        "email": email,
        "borrowed_books": []
    })


def search_books(query):
    query = query.lower()
    results = []
    for isbn, info in books.items():
        if query in info["title"].lower() or query in info["author"].lower():
            results.append({**info, "isbn": isbn})
    return results


def update_book(isbn, title=None, author=None, genre=None, total_copies=None):
    if not _book_exists(isbn):
        raise KeyError(f"Book with ISBN {isbn} not found.")
    book = books[isbn]
    if title is not None:
        book["title"] = title
    if author is not None:
        book["author"] = author
    if genre is not None:
        if genre not in GENRES:
            raise ValueError(f"Invalid genre: {genre}")
        book["genre"] = genre
    if total_copies is not None:
        if total_copies < 0:
            raise ValueError("Total copies cannot be negative.")
        # Ensure we don't reduce below number of borrowed copies
        borrowed_count = sum(1 for m in members for b in m["borrowed_books"] if b == isbn)
        if total_copies < borrowed_count:
            raise ValueError(f"Cannot reduce copies below {borrowed_count} (currently borrowed).")
        book["total_copies"] = total_copies


def update_member(member_id, name=None, email=None):
    member = _find_member(member_id)
    if not member:
        raise KeyError(f"Member {member_id} not found.")
    if name is not None:
        member["name"] = name
    if email is not None:
        member["email"] = email


def delete_book(isbn):
    if not _book_exists(isbn):
        raise KeyError(f"Book {isbn} not found.")
    # Check if any member has borrowed it
    for m in members:
        if isbn in m["borrowed_books"]:
            raise ValueError(f"Cannot delete book {isbn} — it is currently borrowed.")
    del books[isbn]


def delete_member(member_id):
    member = _find_member(member_id)
    if not member:
        raise KeyError(f"Member {member_id} not found.")
    if member["borrowed_books"]:
        raise ValueError(f"Cannot delete member {member_id} — they have borrowed books.")
    members[:] = [m for m in members if m["member_id"] != member_id]


def borrow_book(member_id, isbn):
    member = _find_member(member_id)
    if not member:
        raise KeyError(f"Member {member_id} not found.")
    if not _book_exists(isbn):
        raise KeyError(f"Book {isbn} not found.")

    # Check borrow limit
    if len(member["borrowed_books"]) >= 3:
        raise ValueError(f"Member {member_id} has reached the 3-book borrow limit.")

    # Check availability
    available = books[isbn]["total_copies"] - sum(
        1 for m in members for b in m["borrowed_books"] if b == isbn
    )
    if available <= 0:
        raise ValueError(f"No copies of {isbn} available to borrow.")

    member["borrowed_books"].append(isbn)


def return_book(member_id, isbn):
    member = _find_member(member_id)
    if not member:
        raise KeyError(f"Member {member_id} not found.")
    if isbn not in member["borrowed_books"]:
        raise ValueError(f"Member {member_id} has not borrowed book {isbn}.")
    member["borrowed_books"].remove(isbn)