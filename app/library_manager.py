import json
from typing import List
from app.models import Book

DATA_FILE = "data/library_data.json"

class BookManager:
    def __init__(self):
        try:
            with open(DATA_FILE, "r") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.books, f, indent=4)

    def get_all_books(self) -> List[Book]:
        return self.books

    def get_book(self, book_id: int):
        return next((b for b in self.books if b["id"] == book_id), None)

    def add_book(self, book: Book):
        self.books.append(book.model_dump())
        self.save_data()
        return book

    def update_book(self, book_id: int, updated_book: Book):
        for i, b in enumerate(self.books):
            if b["id"] == book_id:
                self.books[i] = updated_book.model_dump()
                self.save_data()
                return updated_book
        return None

    def delete_book(self, book_id: int):
        self.books = [b for b in self.books if b["id"] != book_id]
        self.save_data()
