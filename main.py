from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["books_db"]
collection = db["books"]

# Book model
class Book(BaseModel):
    title: str
    author: str

# Create a book
@app.post("/books")
def create_book(book: Book):
    book_data = {"title": book.title, "author": book.author}
    result = collection.insert_one(book_data)
    book_id = str(result.inserted_id)
    return {"message": "Book created", "book_id": book_id}

# Get all books
@app.get("/books")
def get_all_books():
    books = []
    for book in collection.find():
        book["_id"] = str(book["_id"])
        books.append(book)
    return books

# Get a specific book
@app.get("/books/{book_id}")
def get_book(book_id: str):
    book = collection.find_one({"_id": ObjectId(book_id)})
    if book:
        book["_id"] = str(book["_id"])
        return book
    return {"message": "Book not found"}

# Update a book
@app.put("/books/{book_id}")
def update_book(book_id: str, book: Book):
    book_data = {"title": book.title, "author": book.author}
    result = collection.update_one({"_id": ObjectId(book_id)}, {"$set": book_data})
    if result.modified_count:
        return {"message": "Book updated"}
    return {"message": "Book not found"}

# Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: str):
    result = collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count:
        return {"message": "Book deleted"}
    return {"message": "Book not found"}