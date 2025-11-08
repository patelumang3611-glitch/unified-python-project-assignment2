#!/bin/bash

echo "Starting Library Management API Tests..."
echo "========================================"

# Start the server in background
echo "Starting server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
SERVER_PID=$!

# Wait for server to start
sleep 5

echo ""
echo "Testing Health Endpoint:"
curl -X GET "http://localhost:8000/health"

echo ""
echo ""
echo "Testing Book Endpoints:"
echo "-----------------------"

# Add a book
echo "1. Adding a book:"
curl -X POST "http://localhost:8000/books" \
     -H "Content-Type: application/json" \
     -d '{"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925}'

echo ""
echo "2. Getting all books:"
curl -X GET "http://localhost:8000/books"

echo ""
echo "3. Getting book by ID:"
curl -X GET "http://localhost:8000/books/1"

echo ""
echo "4. Updating a book:"
curl -X PUT "http://localhost:8000/books/1" \
     -H "Content-Type: application/json" \
     -d '{"id": 1, "title": "The Great Gatsby - Updated", "author": "F. Scott Fitzgerald", "year": 1925}'

echo ""
echo "5. Testing error case - Get non-existent book:"
curl -X GET "http://localhost:8000/books/999"

echo ""
echo ""
echo "Testing Reader Endpoints:"
echo "-------------------------"

# Add a reader
echo "1. Adding a reader:"
curl -X POST "http://localhost:8000/readers" \
     -H "Content-Type: application/json" \
     -d '{"id": 1, "name": "John Doe", "membership_id": "MEM001"}'

echo ""
echo "2. Getting all readers:"
curl -X GET "http://localhost:8000/readers"

echo ""
echo "3. Testing error case - Get non-existent reader:"
curl -X GET "http://localhost:8000/readers/999"

echo ""
echo ""
echo "Testing Staff Endpoints:"
echo "-----------------------"

# Add a staff member
echo "1. Adding a staff member:"
curl -X POST "http://localhost:8000/staff" \
     -H "Content-Type: application/json" \
     -d '{"id": 1, "name": "Jane Smith", "position": "Librarian"}'

echo ""
echo "2. Getting all staff:"
curl -X GET "http://localhost:8000/staff"

echo ""
echo "3. Testing error case - Get non-existent staff:"
curl -X GET "http://localhost:8000/staff/999"

echo ""
echo ""
echo "Final Health Check:"
curl -X GET "http://localhost:8000/health"

echo ""
echo ""
echo "Tests completed. Stopping server..."
kill $SERVER_PID 2>/dev/null

echo "Log file content:"
echo "================="
tail -20 app.log 2>/dev/null || echo "No log file found"
