# tests.py - Unit tests using assert

from operations import (
    add_book, add_member, search_books,
    update_book, delete_book, delete_member,
    borrow_book, return_book,
    books, members, GENRES
)


def reset_data():
    books.clear()
    members.clear()


def test_add_book():
    reset_data()
    add_book("123", "Test Book", "Author", "Fiction", 2)
    assert books["123"]["title"] == "Test Book"
    assert books["123"]["total_copies"] == 2


def test_invalid_genre():
    reset_data()
    try:
        add_book("123", "Bad", "Me", "Horror", 1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_borrow_limit():
    reset_data()
    add_member("M1", "User", "u@test.com")
    add_book("B1", "Book1", "A", "Fiction", 1)
    add_book("B2", "Book2", "A", "Fiction", 1)
    add_book("B3", "Book3", "A", "Fiction", 1)
    add_book("B4", "Book4", "A", "Fiction", 1)

    borrow_book("M1", "B1")
    borrow_book("M1", "B2")
    borrow_book("M1", "B3")

    try:
        borrow_book("M1", "B4")
        assert False, "Should not allow 4th borrow"
    except ValueError:
        pass


def test_no_copies_to_borrow():
    reset_data()
    add_member("M1", "User", "u@test.com")
    add_book("B1", "Book", "A", "Fiction", 1)
    borrow_book("M1", "B1")

    add_member("M2", "User2", "u2@test.com")
    try:
        borrow_book("M2", "B1")
        assert False, "Should not allow borrowing when 0 copies left"
    except ValueError:
        pass


def test_delete_borrowed_book():
    reset_data()
    add_member("M1", "User", "u@test.com")
    add_book("B1", "Book", "A", "Fiction", 1)
    borrow_book("M1", "B1")

    try:
        delete_book("B1")
        assert False, "Should not delete borrowed book"
    except ValueError:
        pass

    return_book("M1", "B1")
    delete_book("B1")
    assert "B1" not in books


# Run all tests
if __name__ == "__main__":
    test_add_book()
    test_invalid_genre()
    test_borrow_limit()
    test_no_copies_to_borrow()
    test_delete_borrowed_book()
    print("✅ All 5 tests passed!")