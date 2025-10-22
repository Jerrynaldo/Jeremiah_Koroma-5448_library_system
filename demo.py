# main.py - Interactive Mini Library Management System

from operations import (
    add_book, add_member, search_books,
    update_book, update_member,
    delete_book, delete_member,
    borrow_book, return_book,
    books, members, GENRES
)

def display_books():
    if not books:
        print("\n📚 No books in the library.")
        return
    print("\n📚 Library Books:")
    print("-" * 80)
    for isbn, info in books.items():
        borrowed_count = sum(1 for m in members for b in m["borrowed_books"] if b == isbn)
        available = info["total_copies"] - borrowed_count
        print(f"ISBN: {isbn}")
        print(f"  Title: {info['title']}")
        print(f"  Author: {info['author']}")
        print(f"  Genre: {info['genre']}")
        print(f"  Copies: {info['total_copies']} (Available: {available})")
        print("-" * 80)

def display_members():
    if not members:
        print("\n👥 No members registered.")
        return
    print("\n👥 Library Members:")
    print("-" * 60)
    for m in members:
        borrowed = ', '.join(m['borrowed_books']) if m['borrowed_books'] else "None"
        print(f"ID: {m['member_id']} | Name: {m['name']} | Email: {m['email']}")
        print(f"  Borrowed Books (ISBNs): [{borrowed}]")
        print("-" * 60)

def get_input(prompt):
    return input(prompt).strip()

def safe_int_input(prompt, min_val=None):
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Value must be at least {min_val}.")
                continue
            return val
        except ValueError:
            print("Please enter a valid number.")

def main():
    print("🏛️  Welcome to the Mini Library Management System!")
    while True:
        print("\n" + "="*50)
        print("Select an option:")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Search Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Update Book")
        print("7. Update Member")
        print("8. Delete Book")
        print("9. Delete Member")
        print("10. View All Books")
        print("11. View All Members")
        print("0. Exit")
        print("="*50)

        choice = get_input("Enter your choice (0-11): ")

        try:
            if choice == "1":
                isbn = get_input("Enter ISBN: ")
                title = get_input("Enter Title: ")
                author = get_input("Enter Author: ")
                print(f"Available genres: {', '.join(GENRES)}")
                genre = get_input("Enter Genre: ")
                copies = safe_int_input("Enter Total Copies: ", min_val=0)
                add_book(isbn, title, author, genre, copies)
                print("✅ Book added successfully!")

            elif choice == "2":
                member_id = get_input("Enter Member ID: ")
                name = get_input("Enter Name: ")
                email = get_input("Enter Email: ")
                add_member(member_id, name, email)
                print("✅ Member added successfully!")

            elif choice == "3":
                query = get_input("Enter title or author to search: ")
                results = search_books(query)
                if results:
                    print(f"\n🔍 Found {len(results)} book(s):")
                    for r in results:
                        print(f"  - {r['title']} by {r['author']} (ISBN: {r['isbn']})")
                else:
                    print("❌ No books found.")

            elif choice == "4":
                member_id = get_input("Enter Member ID: ")
                isbn = get_input("Enter Book ISBN to borrow: ")
                borrow_book(member_id, isbn)
                print("📥 Book borrowed successfully!")

            elif choice == "5":
                member_id = get_input("Enter Member ID: ")
                isbn = get_input("Enter Book ISBN to return: ")
                return_book(member_id, isbn)
                print("📤 Book returned successfully!")

            elif choice == "6":
                isbn = get_input("Enter ISBN of book to update: ")
                if isbn not in books:
                    print("❌ Book not found.")
                    continue
                print("Leave blank to keep current value.")
                title = get_input(f"New Title (current: {books[isbn]['title']}): ") or None
                author = get_input(f"New Author (current: {books[isbn]['author']}): ") or None
                print(f"Genres: {', '.join(GENRES)}")
                genre = get_input(f"New Genre (current: {books[isbn]['genre']}): ") or None
                copies_input = get_input(f"New Total Copies (current: {books[isbn]['total_copies']}): ")
                copies = int(copies_input) if copies_input.isdigit() else None
                update_book(isbn, title=title, author=author, genre=genre, total_copies=copies)
                print("✏️  Book updated successfully!")

            elif choice == "7":
                member_id = get_input("Enter Member ID to update: ")
                member = next((m for m in members if m["member_id"] == member_id), None)
                if not member:
                    print("❌ Member not found.")
                    continue
                print("Leave blank to keep current value.")
                name = get_input(f"New Name (current: {member['name']}): ") or None
                email = get_input(f"New Email (current: {member['email']}): ") or None
                update_member(member_id, name=name, email=email)
                print("✏️  Member updated successfully!")

            elif choice == "8":
                isbn = get_input("Enter ISBN of book to delete: ")
                delete_book(isbn)
                print("🗑️  Book deleted successfully!")

            elif choice == "9":
                member_id = get_input("Enter Member ID to delete: ")
                delete_member(member_id)
                print("🗑️  Member deleted successfully!")

            elif choice == "10":
                display_books()

            elif choice == "11":
                display_members()

            elif choice == "0":
                print("👋 Thank you for using the Library System. Goodbye!")
                break

            else:
                print("❌ Invalid choice. Please enter a number between 0 and 11.")

        except Exception as e:
            print(f"⚠️  Error: {e}")

if __name__ == "__main__":
    main()