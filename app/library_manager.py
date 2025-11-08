import json
import logging
from typing import List
from app.models import Book

logger = logging.getLogger("api")

class BookManager:
    def __init__(self):
        self.data_file = "app/data/books.json"
        self.books = self._load_books()

    def _load_books(self) -> List[dict]:
        """Load books from JSON file"""
        try:
            with open(self.data_file, "r") as f:
                books_data = json.load(f)
                logger.info(f"Loaded {len(books_data)} books from file")
                return books_data
        except FileNotFoundError:
            logger.warning("Books data file not found, starting with empty list")
            return []
        except json.JSONDecodeError:
            logger.error("Error decoding books JSON, starting with empty list")
            return []

    def save_data(self):
        """Save books to JSON file"""
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.books, f, indent=4)
            logger.debug("Books data saved successfully")
        except Exception as e:
            logger.error(f"Error saving books data: {e}")
            raise

    def get_all_books(self) -> List[dict]:
        """Get all books"""
        return self.books

    def get_book(self, book_id: int) -> dict:
        """Get book by ID"""
        book = next((b for b in self.books if b["id"] == book_id), None)
        if book:
            logger.debug(f"Retrieved book with ID: {book_id}")
        else:
            logger.debug(f"Book with ID {book_id} not found")
        return book

    def add_book(self, book: Book) -> dict:
        """Add a new book"""
        book_dict = book.model_dump()
        
        # Check if book with same ID already exists
        if any(b["id"] == book_dict["id"] for b in self.books):
            logger.warning(f"Book with ID {book_dict['id']} already exists")
            raise ValueError(f"Book with ID {book_dict['id']} already exists")
        
        self.books.append(book_dict)
        self.save_data()
        logger.info(f"Added new book: {book_dict}")
        return book_dict

    def update_book(self, book_id: int, updated_book: Book) -> dict:
        """Update an existing book"""
        for i, book in enumerate(self.books):
            if book["id"] == book_id:
                self.books[i] = updated_book.model_dump()
                self.save_data()
                logger.info(f"Updated book with ID: {book_id}")
                return self.books[i]
        
        logger.warning(f"Book with ID {book_id} not found for update")
        return None

    def delete_book(self, book_id: int):
        """Delete a book by ID"""
        initial_count = len(self.books)
        self.books = [book for book in self.books if book["id"] != book_id]
        
        if len(self.books) < initial_count:
            self.save_data()
            logger.info(f"Deleted book with ID: {book_id}")
        else:
            logger.warning(f"Book with ID {book_id} not found for deletion")