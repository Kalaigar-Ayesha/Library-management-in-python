import json

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True
    
    def __str__(self):
        return f"{self.title} by {self.author} - {'Available' if self.available else 'Borrowed'}"

class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []
    
    def borrow_book(self, book):
        if book.available:
            book.available = False
            self.borrowed_books.append(book)
            print(f"{self.name} borrowed {book.title}")
        else:
            print(f"Sorry, {book.title} is already borrowed.")
    
    def return_book(self, book):
        if book in self.borrowed_books:
            book.available = True
            self.borrowed_books.remove(book)
            print(f"{self.name} returned {book.title}")
        else:
            print(f"{self.name} does not have {book.title} to return.")

class Library:
    def __init__(self):
        self.books = []
        self.users = {}
        self.load_data()
    
    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)
        self.save_data()
        print(f"Added book: {book}")
    
    def register_user(self, user_name):
        if user_name not in self.users:
            self.users[user_name] = User(user_name)
            self.save_data()
            print(f"User {user_name} registered successfully.")
        else:
            print("User already exists.")
    
    def display_books(self):
        for book in self.books:
            print(book)
    
    def search_book(self, title):
        found_books = [book for book in self.books if title.lower() in book.title.lower()]
        if found_books:
            for book in found_books:
                print(book)
        else:
            print("No books found matching your search.")
    
    def save_data(self):
        data = {
            "books": [{"title": book.title, "author": book.author, "available": book.available} for book in self.books],
            "users": list(self.users.keys())
        }
        with open("library_data.json", "w") as file:
            json.dump(data, file)
    
    def load_data(self):
        try:
            with open("library_data.json", "r") as file:
                data = json.load(file)
                for book in data.get("books", []):
                    new_book = Book(book["title"], book["author"])
                    new_book.available = book["available"]
                    self.books.append(new_book)
                for user_name in data.get("users", []):
                    self.users[user_name] = User(user_name)
        except FileNotFoundError:
            pass

    def cli_menu(self):
        while True:
            print("\nLibrary Management System")
            print("1. Add Book")
            print("2. Register User")
            print("3. Display Books")
            print("4. Search Book")
            print("5. Borrow Book")
            print("6. Return Book")
            print("7. Exit")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                self.add_book(title, author)
            elif choice == "2":
                user_name = input("Enter user name: ")
                self.register_user(user_name)
            elif choice == "3":
                self.display_books()
            elif choice == "4":
                title = input("Enter book title to search: ")
                self.search_book(title)
            elif choice == "5":
                user_name = input("Enter user name: ")
                title = input("Enter book title to borrow: ")
                if user_name in self.users:
                    user = self.users[user_name]
                    for book in self.books:
                        if book.title.lower() == title.lower():
                            user.borrow_book(book)
                            break
                    else:
                        print("Book not found.")
                else:
                    print("User not registered.")
            elif choice == "6":
                user_name = input("Enter user name: ")
                title = input("Enter book title to return: ")
                if user_name in self.users:
                    user = self.users[user_name]
                    for book in user.borrowed_books:
                        if book.title.lower() == title.lower():
                            user.return_book(book)
                            break
                    else:
                        print("Book not found in user's borrowed list.")
                else:
                    print("User not registered.")
            elif choice == "7":
                print("Exiting Library System. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

# Example Usage
if __name__ == "__main__":
    library = Library()
    library.cli_menu()
