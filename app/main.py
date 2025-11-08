import logging
import time
from fastapi import FastAPI, HTTPException, Request
from app.models import Book, Reader, Staff
from app.library_manager import BookManager
from app.reader_manager import ReaderManager
from app.staff_manager import StaffManager

# -------------------------
# Logging Configuration
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    filemode='a'  # Append mode
)

# Create logger for API
api_logger = logging.getLogger("api")

# -------------------------
# App initialization
# -------------------------
app = FastAPI(title="Library Management System")
book_manager = BookManager()
reader_manager = ReaderManager()
staff_manager = StaffManager()

# -------------------------
# Enhanced Middleware for logging
# -------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request details
    body = await request.body()
    api_logger.info(f"Request: {request.method} {request.url.path} - Body: {body.decode() if body else 'None'}")
    
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        
        # Log response details
        api_logger.info(f"Response: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.2f}ms")
        
        return response
    except Exception as e:
        api_logger.error(f"Error: {request.method} {request.url.path} - {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# -------------------------
# Request Counter for Monitoring
# -------------------------
request_counter = {
    "total": 0,
    "by_endpoint": {},
    "errors": 0
}

def increment_counter(endpoint: str, is_error: bool = False):
    request_counter["total"] += 1
    request_counter["by_endpoint"][endpoint] = request_counter["by_endpoint"].get(endpoint, 0) + 1
    if is_error:
        request_counter["errors"] += 1

# -------------------------
# Root & Health Endpoints
# -------------------------
@app.get("/")
def root():
    increment_counter("/")
    return {"message": "Welcome to the Library Management API"}

@app.get("/health")
def health():
    health_status = {
        "status": "healthy",
        "total_requests": request_counter["total"],
        "requests_by_endpoint": request_counter["by_endpoint"],
        "total_errors": request_counter["errors"]
    }
    return health_status

# -------------------------
# Book Endpoints
# -------------------------
@app.get("/books")
def get_books():
    increment_counter("/books")
    try:
        books = book_manager.get_all_books()
        api_logger.info(f"Retrieved {len(books)} books")
        return books
    except Exception as e:
        increment_counter("/books", is_error=True)
        api_logger.error(f"Error retrieving books: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving books")

@app.get("/books/{book_id}")
def get_book(book_id: int):
    increment_counter(f"/books/{book_id}")
    try:
        book = book_manager.get_book(book_id)
        if not book:
            increment_counter(f"/books/{book_id}", is_error=True)
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    except HTTPException:
        raise
    except Exception as e:
        increment_counter(f"/books/{book_id}", is_error=True)
        api_logger.error(f"Error retrieving book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving book")

@app.post("/books")
def add_book(book: Book):
    increment_counter("/books", is_error=False)
    try:
        result = book_manager.add_book(book)
        api_logger.info(f"Added new book: {book.title} with ID: {book.id}")
        return result
    except Exception as e:
        increment_counter("/books", is_error=True)
        api_logger.error(f"Error adding book: {e}")
        raise HTTPException(status_code=500, detail="Error adding book")

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    increment_counter(f"/books/{book_id}")
    try:
        book = book_manager.update_book(book_id, updated_book)
        if not book:
            increment_counter(f"/books/{book_id}", is_error=True)
            raise HTTPException(status_code=404, detail="Book not found")
        api_logger.info(f"Updated book with ID: {book_id}")
        return book
    except HTTPException:
        raise
    except Exception as e:
        increment_counter(f"/books/{book_id}", is_error=True)
        api_logger.error(f"Error updating book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating book")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    increment_counter(f"/books/{book_id}")
    try:
        book_manager.delete_book(book_id)
        api_logger.info(f"Deleted book with ID: {book_id}")
        return {"message": "Book deleted successfully"}
    except Exception as e:
        increment_counter(f"/books/{book_id}", is_error=True)
        api_logger.error(f"Error deleting book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting book")

# -------------------------
# Reader Endpoints
# -------------------------
@app.get("/readers")
def get_readers():
    increment_counter("/readers")
    try:
        readers = reader_manager.get_all_readers()
        api_logger.info(f"Retrieved {len(readers)} readers")
        return readers
    except Exception as e:
        increment_counter("/readers", is_error=True)
        api_logger.error(f"Error retrieving readers: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving readers")

@app.get("/readers/{reader_id}")
def get_reader(reader_id: int):
    increment_counter(f"/readers/{reader_id}")
    try:
        reader = reader_manager.get_reader(reader_id)
        if not reader:
            increment_counter(f"/readers/{reader_id}", is_error=True)
            raise HTTPException(status_code=404, detail="Reader not found")
        return reader
    except HTTPException:
        raise
    except Exception as e:
        increment_counter(f"/readers/{reader_id}", is_error=True)
        api_logger.error(f"Error retrieving reader {reader_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving reader")

@app.post("/readers")
def add_reader(reader: Reader):
    increment_counter("/readers")
    try:
        result = reader_manager.add_reader(reader)
        api_logger.info(f"Added new reader: {reader.name} with ID: {reader.id}")
        return result
    except Exception as e:
        increment_counter("/readers", is_error=True)
        api_logger.error(f"Error adding reader: {e}")
        raise HTTPException(status_code=500, detail="Error adding reader")

@app.put("/readers/{reader_id}")
def update_reader(reader_id: int, updated_reader: Reader):
    increment_counter(f"/readers/{reader_id}")
    try:
        reader = reader_manager.update_reader(reader_id, updated_reader)
        if not reader:
            increment_counter(f"/readers/{reader_id}", is_error=True)
            raise HTTPException(status_code=404, detail="Reader not found")
        api_logger.info(f"Updated reader with ID: {reader_id}")
        return reader
    except HTTPException:
        raise
    except Exception as e:
        increment_counter(f"/readers/{reader_id}", is_error=True)
        api_logger.error(f"Error updating reader {reader_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating reader")

@app.delete("/readers/{reader_id}")
def delete_reader(reader_id: int):
    increment_counter(f"/readers/{reader_id}")
    try:
        reader_manager.delete_reader(reader_id)
        api_logger.info(f"Deleted reader with ID: {reader_id}")
        return {"message": "Reader deleted successfully"}
    except Exception as e:
        increment_counter(f"/readers/{reader_id}", is_error=True)
        api_logger.error(f"Error deleting reader {reader_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting reader")

# -------------------------
# Staff Endpoints
# -------------------------
@app.get("/staff")
def get_staff():
    increment_counter("/staff")
    try:
        staff = staff_manager.get_all_staff()
        api_logger.info(f"Retrieved {len(staff)} staff members")
        return staff
    except Exception as e:
        increment_counter("/staff", is_error=True)
        api_logger.error(f"Error retrieving staff: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving staff")

@app.get("/staff/{staff_id}")
def get_staff_member(staff_id: int):
    increment_counter(f"/staff/{staff_id}")
    try:
        staff = staff_manager.get_staff(staff_id)
        if not staff:
            increment_counter(f"/staff/{staff_id}", is_error=True)
            raise HTTPException(status_code=404, detail="Staff not found")
        return staff
    except HTTPException:
        raise
    except Exception as e:
        increment_counter(f"/staff/{staff_id}", is_error=True)
        api_logger.error(f"Error retrieving staff {staff_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving staff")

@app.post("/staff")
def add_staff(staff: Staff):
    increment_counter("/staff")
    try:
        result = staff_manager.add_staff(staff)
        api_logger.info(f"Added new staff: {staff.name} with ID: {staff.id}")
        return result
    except Exception as e:
        increment_counter("/staff", is_error=True)
        api_logger.error(f"Error adding staff: {e}")
        raise HTTPException(status_code=500, detail="Error adding staff")

@app.put("/staff/{staff_id}")
def update_staff(staff_id: int, updated_staff: Staff):
    increment_counter(f"/staff/{staff_id}")
    try:
        staff = staff_manager.update_staff(staff_id, updated_staff)
        if not staff:
            increment_counter(f"/staff/{staff_id}", is_error=True)
            raise HTTPException(status_code=404, detail="Staff not found")
        api_logger.info(f"Updated staff with ID: {staff_id}")
        return staff
    except HTTPException:
        raise
    except Exception as e:
        increment_counter(f"/staff/{staff_id}", is_error=True)
        api_logger.error(f"Error updating staff {staff_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating staff")

@app.delete("/staff/{staff_id}")
def delete_staff(staff_id: int):
    increment_counter(f"/staff/{staff_id}")
    try:
        staff_manager.delete_staff(staff_id)
        api_logger.info(f"Deleted staff with ID: {staff_id}")
        return {"message": "Staff deleted successfully"}
    except Exception as e:
        increment_counter(f"/staff/{staff_id}", is_error=True)
        api_logger.error(f"Error deleting staff {staff_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting staff")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)