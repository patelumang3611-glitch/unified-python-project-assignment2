import logging
import time
from fastapi import FastAPI, HTTPException, Request
from app.models import Book, Reader, Staff
from app.library_manager import BookManager
from app.reader_manager import ReaderManager
from app.staff_manager import StaffManager

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------
# App initialization
# -------------------------
app = FastAPI(title="Library Management System")
book_manager = BookManager()
reader_manager = ReaderManager()
staff_manager = StaffManager()

# -------------------------
# Middleware for logging
# -------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logging.info(f"{request.method} {request.url.path} - Request received")
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logging.info(f"{request.method} {request.url.path} - Response: {response.status_code} ({process_time:.2f}ms)")
        return response
    except Exception as e:
        logging.error(f"Error on {request.method} {request.url.path} - {e}")
        raise e

# -------------------------
# Root & Health
# -------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Library Management API"}

@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------
# Book Endpoints
# -------------------------
@app.get("/books")
def get_books():
    return book_manager.get_all_books()

@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = book_manager.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books")
def add_book(book: Book):
    return book_manager.add_book(book)

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    book = book_manager.update_book(book_id, updated_book)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book_manager.delete_book(book_id)
    return {"message": "Book deleted successfully"}

# -------------------------
# Reader Endpoints
# -------------------------
@app.get("/readers")
def get_readers():
    return reader_manager.get_all_readers()

@app.get("/readers/{reader_id}")
def get_reader(reader_id: int):
    reader = reader_manager.get_reader(reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

@app.post("/readers")
def add_reader(reader: Reader):
    return reader_manager.add_reader(reader)

@app.put("/readers/{reader_id}")
def update_reader(reader_id: int, updated_reader: Reader):
    reader = reader_manager.update_reader(reader_id, updated_reader)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

@app.delete("/readers/{reader_id}")
def delete_reader(reader_id: int):
    reader_manager.delete_reader(reader_id)
    return {"message": "Reader deleted successfully"}

# -------------------------
# Staff Endpoints
# -------------------------
@app.get("/staff")
def get_staff():
    return staff_manager.get_all_staff()

@app.get("/staff/{staff_id}")
def get_staff_member(staff_id: int):
    staff = staff_manager.get_staff(staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@app.post("/staff")
def add_staff(staff: Staff):
    return staff_manager.add_staff(staff)

@app.put("/staff/{staff_id}")
def update_staff(staff_id: int, updated_staff: Staff):
    staff = staff_manager.update_staff(staff_id, updated_staff)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@app.delete("/staff/{staff_id}")
def delete_staff(staff_id: int):
    staff_manager.delete_staff(staff_id)
    return {"message": "Staff deleted successfully"}
